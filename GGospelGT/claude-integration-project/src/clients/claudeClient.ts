class ClaudeClient {
    private apiKey: string;
    private baseUrl: string;

    constructor(apiKey: string, baseUrl: string = 'https://api.claude.ai') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
    }

    public async sendRequest(endpoint: string, data: any): Promise<any> {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.apiKey}`
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status} ${response.statusText}`);
        }

        return response.json();
    }

    public setApiKey(apiKey: string): void {
        this.apiKey = apiKey;
    }

    public getBaseUrl(): string {
        return this.baseUrl;
    }

    public setBaseUrl(baseUrl: string): void {
        this.baseUrl = baseUrl;
    }
}