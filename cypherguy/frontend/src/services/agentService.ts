/**
 * Agent Service - Connect to IntakeAgent for chat functionality
 * Falls back to mock if connection fails
 */

const INTAKE_AGENT_URL = import.meta.env.VITE_INTAKE_AGENT_URL || 'https://cypherguy-1.onrender.com';
const USE_MOCK = import.meta.env.VITE_USE_MOCK_AGENT === 'true'; // Set to 'true' to force mock

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
 * Falls back to mock if USE_MOCK is true or connection fails
 */
export async function sendChatMessage(message: string, userId: string = 'default_user'): Promise<ChatResponse> {
  // Use mock if explicitly enabled
  if (USE_MOCK) {
    const { sendChatMessageMock } = await import('./agentServiceMock');
    return sendChatMessageMock(message, userId);
  }

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
    console.warn('IntakeAgent connection failed, using mock:', error);
    // Fallback to mock on error
    const { sendChatMessageMock } = await import('./agentServiceMock');
    return sendChatMessageMock(message, userId);
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

