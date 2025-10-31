import { useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Layout from '@/components/Layout';
import ChatMessage from '@/components/ChatMessage';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Sparkles } from 'lucide-react';
import { sendChatMessage } from '@/services/agentService';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
}

export default function Chat() {
  const location = useLocation();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hey there! I'm CypherGuy, your AI DeFi assistant. Ask me anything about your portfolio, trading, loans, or any DeFi questions!",
    },
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [hasInitialMessage, setHasInitialMessage] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = async (messageText: string) => {
    if (!messageText.trim() || isTyping) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText,
    };

    // Add user message first to get full context
    setMessages((prev) => [...prev, userMessage]);
    setIsTyping(true);

    try {
      // Call mock service with conversation history for context (including the just-added message)
      const response = await sendChatMessage(
        messageText, 
        'user',
        [...messages, userMessage].map(m => ({ role: m.role, content: m.content }))
      );
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response || 'Sorry, I could not process that request.',
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again later!',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;
    const messageText = input;
    setInput('');
    await handleSendMessage(messageText);
  };

  // Handle initial message from navigation
  useEffect(() => {
    const initialMessage = (location.state as { initialMessage?: string })?.initialMessage;
    if (initialMessage && !hasInitialMessage) {
      setHasInitialMessage(true);
      // Small delay to ensure UI is ready
      setTimeout(() => {
        handleSendMessage(initialMessage);
      }, 500);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state, hasInitialMessage]);

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Layout>
      <div className="max-w-2xl mx-auto h-[calc(100vh-12rem)] flex flex-col">
        {/* Chat Header */}
        <div className="pb-4 border-b border-border/50 mb-4">
          <div className="flex items-center gap-3">
            <Sparkles className="w-6 h-6 text-primary" />
            <div>
              <h1 className="text-xl font-bold">Chat with CypherGuy</h1>
              <p className="text-sm text-muted-foreground">AI-powered DeFi assistant</p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
          {messages.map((message) => (
            <ChatMessage key={message.id} {...message} />
          ))}
          {isTyping && (
            <ChatMessage role="assistant" content="" isTyping />
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="glass-card p-3 rounded-2xl flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me anything about your DeFi portfolio..."
            className="flex-1 bg-transparent border-0 focus-visible:ring-0 text-sm"
            disabled={isTyping}
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            size="icon"
            variant="default"
            className="flex-shrink-0"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </Layout>
  );
}
