export default function Header() {
    return (
        <div
            className="fixed top-0 left-0 right-0 z-40 flex items-center justify-center py-4"
            style={{
                background: "linear-gradient(to bottom, rgba(0,0,0,0.9) 0%)",
            }}
        >
            <h1
                className="text-3xl font-extrabold tracking-[0.2em] uppercase"
                style={{ color: "rgba(255,255,255,0.75)" }}
            >
                AskPat
            </h1>
        </div>
    )
}