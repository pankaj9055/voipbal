from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# --- State constants ---
LOGIN, ENTER_TXID = range(2)
SUPPORT_ID = "YourSupportTGusername"  # Example: "yourusername" (without @)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔑 Login VoIP Account", callback_data="login")],
        [InlineKeyboardButton("💬 Support", callback_data="support")],
        [InlineKeyboardButton("ℹ️ Bot Usage Guide", callback_data="guide")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Multiline text ek hi line me for mobile/desktop bug prevention
    text = "👋 Welcome to VoIPfit Balance Bot!
Step-by-step use:
1️⃣ Login your VoIP account
2️⃣ Tap Recharge and get Binance USDT address
3️⃣ Send your Binance TXID for instant credit
4️⃣ All balance/progress will show in bot"
    await update.message.reply_text(text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "login":
        await query.edit_message_text("🔐 Please send your VoIP username:")
        return LOGIN
    elif query.data == "support":
        # Change SUPPORT_ID to your Telegram username or group/channel link
        await query.edit_message_text(f"🙋‍♂️ Support Team:
Contact: @{SUPPORT_ID}
Ya yahan apni problem likh ke bhejein, hum turant madad karenge!")
        return ConversationHandler.END
    elif query.data == "guide":
        guide_text = "📝 Bot Usage Guide:

• Login VoIP account via 'Login' button
• Tap 'Recharge' for USDT address
• Send Binance TXID to auto add balance
• Use /balance anytime to view live balance"
        await query.edit_message_text(guide_text)
        return ConversationHandler.END
    elif query.data == "recharge":
        binance_address = "TRX1USDTADDRESS987X"
        await query.edit_message_text(
            f"⬆️ Send USDT on:
<b>{binance_address}</b> (TRC20)

Then paste your <b>transaction hash/ID</b> here:", parse_mode='HTML')
        return ENTER_TXID

async def login_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    # --- VOIP LOGIN API Placeholder ---
    auth_pass = True 
    if auth_pass:
        context.user_data['voip_username'] = username
        keyboard = [
            [InlineKeyboardButton("💸 Recharge", callback_data="recharge")],
            [InlineKeyboardButton("💰 Check Balance", callback_data="balance")],
            [InlineKeyboardButton("💬 Support", callback_data="support")],
            [InlineKeyboardButton("💡 How to Recharge?", callback_data="guide")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"✅ Login Success! Welcome {username}.

Now tap Recharge button below to top-up balance.",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Login failed. Wrong username or API error.")
        return LOGIN

async def txid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txid = update.message.text.strip()
    is_valid = True  # Put API logic here
    if is_valid:
        recharge_done = True  # Put API response logic here
        if recharge_done:
            await update.message.reply_text("🎉 Recharge successful! Balance added to your VoIP account.")
        else:
            await update.message.reply_text("⚠️ Recharge failed, contact support.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ TXID invalid or not yet received. Please check and resend.")
        return ENTER_TXID

async def balance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = context.user_data.get('voip_username', None)
    balance = "450"  # Replace by API response
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(f"💰 Your VoIP Account Balance:
<b>{balance} INR</b>", parse_mode='HTML')

def main():
    app = Application.builder().token("7618685366:AAFEKhRtrcAI_WDv2TcotyfST0YAsVJu52M").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), CallbackQueryHandler(button_handler)],
        states={
            LOGIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, login_handler)],
            ENTER_TXID: [MessageHandler(filters.TEXT & ~filters.COMMAND, txid_handler)],
        },
        fallbacks=[CommandHandler("start", start)],
        allow_reentry=True,
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("balance", balance_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
