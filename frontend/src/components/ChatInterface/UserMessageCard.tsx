import { motion } from "framer-motion";

type UserMessageCardProps = {
  message: string;
  timestamp?: string;
};

export default function UserMessageCard({
  message,
  timestamp,
}: UserMessageCardProps) {
  const time =
    timestamp ??
    new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  return (
    <motion.div
      initial={{ opacity: 0, y: 10, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="flex justify-end w-full px-3 sm:px-4 md:px-6"
    >
      <div className="flex flex-col items-end gap-1 max-w-[85%] sm:max-w-[75%] md:max-w-[65%]">

        {/* Message bubble */}
        <div
          className="px-4 py-3 rounded-2xl rounded-br-sm"
          style={{
            background: "rgba(255,255,255,0.08)",
            border: "1px solid rgba(255,255,255,0.12)",
            backdropFilter: "blur(16px)",
            WebkitBackdropFilter: "blur(16px)",
            boxShadow: "0 4px 24px rgba(0,0,0,0.2)",
          }}
        >
          <p
            className="leading-relaxed whitespace-pre-wrap wrap-break-words"
            style={{
              color: "rgba(255,255,255,0.88)",
              fontSize: "clamp(13px, 1.6vw, 15px)",
            }}
          >
            {message}
          </p>
        </div>

        {/* Timestamp */}
        <span
          style={{
            color: "rgba(255,255,255,0.22)",
            fontSize: "10px",
            paddingRight: "4px",
          }}
        >
          {time}
        </span>

      </div>
    </motion.div>
  );
}