import { useState, useRef, useEffect } from "react"
import ChatBar from "./components/ChatInterface/ChatBar"
import UserMessageCard from "./components/ChatInterface/UserMessageCard"
import AiMessageCard from "./components/ChatInterface/AIMessageCard"
import Sidebar from "./components/ChatInterface/Sidebar/Sidebar"
import Header from "./components/ChatInterface/Header"

type Message = {
  id: number
  role: "user" | "ai"
  text: string
  timestamp: string
}

type Chat = {
  id: number
  title: string
  messages: Message[]
}

const DUMMY_RESPONSE =
  "Sure, I'd be happy to help you with that! Based on what you've described, it sounds like the issue might be related to your account configuration. First, try clearing your browser cache and cookies, then attempt to log in again."

export default function User() {
  const [chats, setChats] = useState<Chat[]>([])
  const [activeChatId, setActiveChatId] = useState<number | null>(null)
  const [isTyping, setIsTyping] = useState(false)
  const streamRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  const activeChat = chats.find((c) => c.id === activeChatId)
  const messages = activeChat?.messages ?? []

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, isTyping])

  const handleNewChat = () => {
    if (streamRef.current) clearTimeout(streamRef.current)
    setIsTyping(false)
    const id = Date.now()
    setChats((prev) => [{ id, title: "New Chat", messages: [] }, ...prev])
    setActiveChatId(id)
  }

  const handleSelectChat = (id: number) => {
    if (streamRef.current) clearTimeout(streamRef.current)
    setIsTyping(false)
    setActiveChatId(id)
  }

  const handleDeleteChat = (id: number) => {
    setChats((prev) => prev.filter((c) => c.id !== id))
    if (activeChatId === id) setActiveChatId(null)
  }

  const handleRenameChat = (id: number, newTitle: string) => {
    setChats((prev) =>
      prev.map((c) => (c.id === id ? { ...c, title: newTitle } : c))
    )
  }

  const streamAiResponse = (chatId: number) => {
    const words = DUMMY_RESPONSE.split(" ")
    let index = 0

    const aiId = Date.now() + 1
    const timestamp = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    })

    setChats((prev) =>
      prev.map((c) =>
        c.id === chatId
          ? {
              ...c,
              messages: [
                ...c.messages,
                { id: aiId, role: "ai" as const, text: "", timestamp },
              ],
            }
          : c
      )
    )

    setIsTyping(false)

    const tick = () => {
      if (index >= words.length) return
      const chunk = words.slice(0, index + 1).join(" ")
      setChats((prev) =>
        prev.map((c) =>
          c.id === chatId
            ? {
                ...c,
                messages: c.messages.map((msg) =>
                  msg.id === aiId ? { ...msg, text: chunk } : msg
                ),
              }
            : c
        )
      )
      index++
      streamRef.current = setTimeout(tick, 45)
    }

    tick()
  }

  const handleSend = (msg: string) => {
    if (streamRef.current) clearTimeout(streamRef.current)

    let chatId = activeChatId
    if (!chatId) {
      chatId = Date.now()
      setChats((prev) => [{ id: chatId!, title: msg.slice(0, 30), messages: [] }, ...prev])
      setActiveChatId(chatId)
    } else {
      setChats((prev) =>
        prev.map((c) =>
          c.id === chatId && c.title === "New Chat"
            ? { ...c, title: msg.slice(0, 30) }
            : c
        )
      )
    }

    const userMsg: Message = {
      id: Date.now() + 2,
      role: "user",
      text: msg,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    }

    setChats((prev) =>
      prev.map((c) =>
        c.id === chatId ? { ...c, messages: [...c.messages, userMsg] } : c
      )
    )

    setIsTyping(true)
    setTimeout(() => streamAiResponse(chatId!), 1000)
  }

  return (
    // Sidebar is fixed so main area takes full width — no flex push
    <div className="w-full h-screen overflow-hidden">

      {/* Sidebar floats above, zero layout impact */}
      <Sidebar
        chats={chats}
        activeChatId={activeChatId ?? undefined}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
        onDeleteChat={handleDeleteChat}
        onRenameChat={handleRenameChat}
        onSettings={() => console.log("settings")}
        onAccount={() => console.log("account")}
      />

      {/* Main area — full width, independent of sidebar */}
      <div className="flex flex-col h-full w-full overflow-hidden">

        <Header />

        {/* Scrollable messages */}
        <div className="flex-1 overflow-y-auto">
          <div className="flex flex-col gap-4 pt-16 pb-36 max-w-3xl w-full mx-auto">

            {/* Empty state */}
            {messages.length === 0 && !isTyping && (
              <div className="flex flex-col items-center justify-center gap-3 mt-24">
                <span style={{ fontSize: "32px", opacity: 0.4 }}>✦</span>
                <p className="text-sm" style={{ color: "rgba(255,255,255,0.25)" }}>
                  Ask Pat anything
                </p>
              </div>
            )}

            {messages.map((msg) =>
              msg.role === "user" ? (
                <UserMessageCard
                  key={msg.id}
                  message={msg.text}
                  timestamp={msg.timestamp}
                />
              ) : (
                <AiMessageCard
                  key={msg.id}
                  message={msg.text}
                  timestamp={msg.timestamp}
                  isLoading={msg.text === "" && !isTyping}
                />
              )
            )}

            {isTyping && <AiMessageCard message="" isLoading timestamp="" />}

            <div ref={bottomRef} />
          </div>
        </div>

        {/* Pinned chatbar */}
        <div
          className="absolute bottom-0 left-0 right-0 pb-5 pt-6"
          style={{
            background: "linear-gradient(to top, rgba(0,0,0,0.85) 60%, transparent)",
          }}
        >
          <ChatBar onSend={handleSend} />
        </div>

      </div>
    </div>
  )
}