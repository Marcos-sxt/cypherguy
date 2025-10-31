/**
 * Agent Service - 100% Mocked (no connection to real agents)
 * Frontend is fully mocked for demo purposes
 */

const INTAKE_AGENT_URL = import.meta.env.VITE_INTAKE_AGENT_URL || 'https://cypherguy-1.onrender.com';
const USE_MOCK = true; // Always use mock - frontend is 100% mocked

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
 * Send a chat message - 100% MOCKED (no real agent connection)
 * Frontend is fully mocked for demo/hackathon purposes
 */
export async function sendChatMessage(
  message: string, 
  userId: string = 'default_user',
  previousMessages?: Array<{ role: string; content: string }>
): Promise<ChatResponse> {
  // Always use mock - frontend is 100% mocked
  const { sendChatMessageMock } = await import('./agentServiceMock');
  return sendChatMessageMock(message, userId, previousMessages);
}

/**
 * Check if IntakeAgent is healthy - MOCKED (always returns true)
 */
export async function checkAgentHealth(): Promise<boolean> {
  // Always return true - frontend is 100% mocked
  return true;
}

