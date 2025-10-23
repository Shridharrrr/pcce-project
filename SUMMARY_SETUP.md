# Chat Summary Feature Setup Guide

This guide will help you set up the AI-powered chat summary feature using **Hugging Face** and **Google Gemini** APIs for dual-layer summarization.

## Prerequisites

1. **Hugging Face Account**: Sign up at [https://huggingface.co/](https://huggingface.co/)
2. **Hugging Face API Token**: Get your API token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. **Google Cloud Account**: Sign up at [https://cloud.google.com/](https://cloud.google.com/)
4. **Gemini API Key**: Get your API key from [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

## Backend Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `requests` - For Hugging Face API calls
- `google-generativeai` - For Gemini API integration

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
cp .env.example .env
```

Edit the `.env` file and add both API keys:

```env
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important**: Never commit your `.env` file to version control!

### 3. Add .env to .gitignore

Make sure your `backend/.gitignore` includes:

```
.env
```

## Features

### 🤖 Dual-Layer AI Summarization

**Two-Stage Process:**

1. **Stage 1 - Hugging Face (BART-large-CNN)**
   - Initial abstractive summarization
   - Processes raw chat messages
   - Generates base summary

2. **Stage 2 - Google Gemini Pro**
   - Refines and enhances the initial summary
   - Identifies key points and action items
   - Creates structured, actionable summaries
   - Adds professional formatting

### 📊 Summary Details

Each summary includes:
- **Gemini Enhanced Summary**: Refined, structured summary with key points and action items
- **Original Summary**: Base summary from Hugging Face (collapsible)
- **Enhancement Status**: Badge showing if Gemini enhancement was successful
- **Total Messages**: Count of all messages analyzed
- **Text Messages**: Count of text-only messages
- **Participants**: List of all conversation participants
- **Timestamp**: When the summary was created
- **Creator**: Who generated the summary

## API Endpoints

### Generate Summary
```
POST /summaries/generate
Body: {
  "team_id": "string",
  "message_count": 100  // optional, defaults to 100
}
```

### Get Team Summaries
```
GET /summaries/team/{team_id}
```

### Get Specific Summary
```
GET /summaries/{summary_id}
```

### Delete Summary
```
DELETE /summaries/{summary_id}
```

## Frontend Usage

### Access Summaries

1. Select a project from the sidebar
2. Click on the **"Summary"** tab
3. Click **"🤖 Generate Summary"** button
4. Wait for the AI to process your chat messages
5. View the generated summary with statistics

### Summary Display

- **Expandable Content**: Long summaries can be expanded/collapsed
- **Statistics Badges**: Quick view of message counts and participants
- **Delete Option**: Remove summaries you no longer need
- **Auto-Refresh**: New summaries appear automatically

## How It Works

1. **User clicks "Generate Summary"**
   - Frontend sends request to `/summaries/generate`
   
2. **Backend fetches messages**
   - Retrieves last 100 messages from Firestore
   - Formats messages with sender names
   
3. **Stage 1: Hugging Face Processing**
   - Sends formatted text to BART-large-CNN model
   - Receives initial AI-generated summary
   - Extracts conversation statistics
   
4. **Stage 2: Gemini Enhancement**
   - Forwards Hugging Face summary to Gemini Pro
   - Gemini refines and structures the summary
   - Identifies key points and action items
   - Creates professional, actionable format
   
5. **Summary saved to Firestore**
   - Stores both summaries (HF + Gemini)
   - Saves metadata and statistics
   - Marks enhancement status
   
6. **Display**
   - Shows Gemini enhanced summary prominently
   - Provides collapsible original summary
   - Displays statistics and participants
   - Offers delete option

## Model Information

### Hugging Face - BART-large-CNN
- **Model**: `facebook/bart-large-cnn`
- **Type**: Abstractive summarization
- **Max Input**: ~5000 characters
- **Output Length**: 30-150 words
- **Purpose**: Initial summary generation

### Google Gemini Pro
- **Model**: `gemini-pro`
- **Type**: Large Language Model
- **Capabilities**: Text refinement, structuring, analysis
- **Output**: Structured summaries with key points and action items
- **Purpose**: Enhancement and refinement of initial summary

## Troubleshooting

### "HUGGINGFACE_API_KEY not found" or "GEMINI_API_KEY not found"
- Ensure `.env` file exists in `backend/` directory
- Check that both keys are correctly formatted
- Restart the backend server after adding the keys

### "Hugging Face API request timed out"
- The model might be loading (cold start)
- Try again after a few seconds
- Check your internet connection

### "No messages to summarize"
- Ensure the team has chat messages
- Check that messages are of type "text"
- Verify you're a member of the team

### Summary shows "enhanced: false"
- Gemini API might have failed
- Check your Gemini API key
- Original Hugging Face summary is still available
- The system gracefully falls back to HF-only summary

### Rate Limiting
- Both APIs have rate limits on free tiers
- Hugging Face: Limited requests per month
- Gemini: Generous free tier with quotas
- Consider upgrading for production use
- Implement caching for frequently accessed summaries

## Best Practices

1. **Generate summaries periodically** rather than for every message
2. **Use meaningful message counts** (50-100 messages work best)
3. **Delete old summaries** to keep the interface clean
4. **Monitor API usage** to avoid rate limits

## Security Notes

- API keys are stored server-side only
- Never expose your Hugging Face API key in frontend code
- Summaries are team-scoped (only members can access)
- Only creators and team admins can delete summaries

## Cost Considerations

- **Free Tier**: Limited requests per month
- **Pro Tier**: Higher rate limits and faster inference
- **Enterprise**: Dedicated infrastructure

Check [Hugging Face Pricing](https://huggingface.co/pricing) for details.

## Future Enhancements

Potential improvements:
- Custom summary length selection
- Multiple model options
- Scheduled automatic summaries
- Summary comparison over time
- Export summaries as PDF/Markdown
- Email summaries to team members

## Support

For issues or questions:
1. Check the console logs (browser and server)
2. Verify API key configuration
3. Test with a small number of messages first
4. Review Hugging Face API status

---

**Enjoy AI-powered chat summaries! 🚀**
