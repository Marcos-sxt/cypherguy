import logo from '@/assets/cypherguy-logo.png';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  isTyping?: boolean;
}

export default function ChatMessage({ role, content, isTyping = false }: ChatMessageProps) {
  return (
    <div
      className={`flex gap-3 animate-fade-in ${
        role === 'user' ? 'justify-end' : 'justify-start'
      }`}
    >
      {role === 'assistant' && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-primary-glow flex items-center justify-center flex-shrink-0 glow-effect">
          <img src={logo} alt="CypherGuy" className="w-5 h-5" />
        </div>
      )}

      <div
        className={`max-w-[75%] px-4 py-3 rounded-2xl ${
          role === 'user'
            ? 'bg-primary text-primary-foreground rounded-br-sm'
            : 'glass-card rounded-bl-sm'
        }`}
      >
        {isTyping ? (
          <div className="flex gap-1.5">
            <span className="w-2 h-2 bg-primary rounded-full typing-indicator" style={{ animationDelay: '0s' }} />
            <span className="w-2 h-2 bg-primary rounded-full typing-indicator" style={{ animationDelay: '0.2s' }} />
            <span className="w-2 h-2 bg-primary rounded-full typing-indicator" style={{ animationDelay: '0.4s' }} />
          </div>
        ) : (
          <p className="text-sm leading-relaxed">{content}</p>
        )}
      </div>

      {role === 'user' && (
        <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center flex-shrink-0">
          <span className="text-sm font-semibold">You</span>
        </div>
      )}
    </div>
  );
}
