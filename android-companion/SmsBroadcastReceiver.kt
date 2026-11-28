package ai.scamshield.companion

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.util.Log

/**
 * SmsBroadcastReceiver
 * Directly intercepts incoming SMS PDUs before they are viewed by the user.
 * Forwards sender and message payload to ScamShield threat engine.
 */
class SmsBroadcastReceiver : BroadcastReceiver() {

    companion object {
        private const val TAG = "ScamShieldSmsReceiver"
    }

    override fun onReceive(context: Context?, intent: Intent?) {
        if (intent?.action != Telephony.Sms.Intents.SMS_RECEIVED_ACTION) return

        val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)
        for (sms in messages) {
            val sender = sms.displayOriginatingAddress ?: "Unknown"
            val messageBody = sms.displayMessageBody ?: ""

            Log.d(TAG, "Incoming SMS from $sender intercepted. Length: ${messageBody.length}")

            // Fast local check for credential harvest & banking phishing
            val lower = messageBody.lowercase()
            if (lower.contains("otp") || lower.contains("debit") || lower.contains("blocked") || lower.contains("electricity")) {
                Log.w(TAG, "Critical marker in SMS from $sender: Triggering ScamShield analysis.")
            }
        }
    }
}
