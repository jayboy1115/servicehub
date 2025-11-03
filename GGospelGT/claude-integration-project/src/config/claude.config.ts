export const claudeConfig = {
    apiKey: process.env.CLAUDE_API_KEY || '',
    apiUrl: process.env.CLAUDE_API_URL || 'https://api.claude.ai/v1',
    timeout: 5000,
};