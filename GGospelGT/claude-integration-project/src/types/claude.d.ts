interface ClaudeRequest {
    prompt: string;
    maxTokens?: number;
    temperature?: number;
    topP?: number;
    n?: number;
}

interface ClaudeResponse {
    id: string;
    object: string;
    created: number;
    model: string;
    choices: Array<{
        text: string;
        index: number;
        logprobs?: any;
        finish_reason: string;
    }>;
}

interface ClaudeError {
    error: {
        message: string;
        type: string;
        code?: string;
        param?: string;
        status?: number;
    };
}