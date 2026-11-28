package ai.scamshield.companion

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import android.util.Log
import androidx.core.app.NotificationCompat

/**
 * ScamShieldNotificationListener
 * Intercepts incoming WhatsApp and SMS notifications with user consent.
 * Evaluates message text for credential extraction, electricity cut-off threats,
 * digital arrest coercion, and bank phishing before the user opens the chat.
 */
class ScamShieldNotificationListener : NotificationListenerService() {

    companion object {
        private const val TAG = "ScamShieldListener"
        private const val CHANNEL_ID = "scamshield_threat_alerts"
        private const val NOTIFICATION_ID = 9110
        
        // Target packages to monitor
        private val MONITORED_PACKAGES = setOf(
            "com.whatsapp",
            "com.whatsapp.w4b", // WhatsApp Business
            "com.google.android.apps.messaging", // Google Messages
            "com.android.mms", // Stock SMS
            "org.telegram.messenger" // Telegram
        )
    }

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        Log.i(TAG, "ScamShield Threat Guard Active in Background.")
    }

    override fun onNotificationPosted(sbn: StatusBarNotification?) {
        if (sbn == null) return

        val packageName = sbn.packageName
        if (!MONITORED_PACKAGES.contains(packageName)) return

        val extras = sbn.notification.extras
        val title = extras.getString("android.title") ?: ""
        val text = extras.getCharSequence("android.text")?.toString() ?: ""

        if (text.isBlank()) return

        // Fast on-device heuristic evaluation (< 2ms)
        val threatScore = evaluateThreatScore(text)

        if (threatScore >= 60) {
            Log.w(TAG, "🚨 THREAT DETECTED ($threatScore%): From $title in $packageName")
            postThreatAlert(title, text, threatScore)
        }
    }

    /**
     * Local lightweight threat evaluator matching ScamShield engine rules
     */
    private fun evaluateThreatScore(text: String): Int {
        val lower = text.lowercase()
        var score = 0

        // Credential harvesting
        if (lower.contains("otp") || lower.contains("cvv") || lower.contains("pin") || lower.contains("password")) {
            score += 45
        }

        // Electricity / Utility cut-off coercion
        if (lower.contains("electricity") || lower.contains("bijli") || lower.contains("disconnected tonight") || lower.contains("power cut")) {
            score += 40
        }

        // Digital arrest / CBI / Police impersonation
        if (lower.contains("digital arrest") || lower.contains("cbi") || lower.contains("narcotics") || lower.contains("customs on hold")) {
            score += 50
        }

        // Urgency triggers
        if (lower.contains("immediately") || lower.contains("within 24 hours") || lower.contains("urgent") || lower.contains("blocked today")) {
            score += 25
        }

        // Suspicious shortlinks or APKs
        if (lower.contains(".apk") || lower.contains("bit.ly") || lower.contains("tinyurl") || lower.contains("ngrok")) {
            score += 35
        }

        return score.coerceAtMost(98)
    }

    /**
     * Posts a High-Priority Heads-Up banner on user lock screen
     */
    private fun postThreatAlert(sender: String, messageSnippet: String, riskScore: Int) {
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // Intent to Dial 1930
        val dialIntent = Intent(Intent.ACTION_DIAL).apply {
            data = Uri.parse("tel:1930")
        }
        val dialPendingIntent = PendingIntent.getActivity(
            this, 0, dialIntent, PendingIntent.FLAG_IMMUTABLE
        )

        // Intent to open ScamShield Web Console for full forensic inspection
        val consoleIntent = Intent(Intent.ACTION_VIEW).apply {
            data = Uri.parse("https://scam-shield-ai-wheat.vercel.app")
        }
        val consolePendingIntent = PendingIntent.getActivity(
            this, 1, consoleIntent, PendingIntent.FLAG_IMMUTABLE
        )

        val alertNotification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.stat_sys_warning)
            .setContentTitle("🚨 SCAM DETECTED ($riskScore% Risk)")
            .setContentText("Warning: Message from $sender contains urgent fraud markers. Do not click links or share OTP!")
            .setStyle(NotificationCompat.BigTextStyle().bigText(
                "Sender: $sender\nRisk Level: CRITICAL ($riskScore%)\nMessage: \"$messageSnippet\"\n\nAction: Block sender immediately. Do not share OTP or PIN."
            ))
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setDefaults(NotificationCompat.DEFAULT_ALL)
            .setAutoCancel(true)
            .addAction(android.R.drawable.ic_menu_call, "Dial 1930 Helpline", dialPendingIntent)
            .addAction(android.R.drawable.ic_menu_view, "Inspect Forensics", consolePendingIntent)
            .build()

        notificationManager.notify(NOTIFICATION_ID, alertNotification)
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "ScamShield Real-Time Fraud Interceptor",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Critical alerts for intercepted WhatsApp & SMS cyber fraud threats"
                enableVibration(true)
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager?.createNotificationChannel(channel)
        }
    }
}
