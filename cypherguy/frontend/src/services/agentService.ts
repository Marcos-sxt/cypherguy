/**
 * Agent Service - Connect to IntakeAgent for chat functionality
 */

const INTAKE_AGENT_URL = import.meta.env.VITE_INTAKE_AGENT_URL || 'https://cypherguy-1.onrender.com';

export interface ChatRequest {
  message: string;
  user_id?: string;
}

export interface ChatResponse {
  response: string;
  user_id: string;
  intent?: string;
  error?: string;
}

/**
 * Send a chat message to IntakeAgent
 */
export async function sendChatMessage(message: string, userId: string = 'default_user'): Promise<ChatResponse> {
  try {
    const response = await fetch(`${INTAKE_AGENT_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        user_id: userId,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data: ChatResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    // Fallback mock response on error
    return {
      response: "Sorry, I'm having trouble connecting right now. Please try again later!",
      user_id: userId,
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
}

/**
 * Check if IntakeAgent is healthy
 */
export async function checkAgentHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${INTAKE_AGENT_URL}/health`);
    return response.ok;
  } catch (error) {
    console.error('Error checking agent health:', error);
    return false;
  }
}

