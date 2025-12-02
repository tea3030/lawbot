import "./App.css";
import { ChatContainer } from "./components/Chat/ChatContainer";
import { Header } from "./components/UI/Header";
import { Footer } from "./components/UI/Footer";
import { ErrorBoundary } from "./components/UI/ErrorBoundary";

function App() {
  return (
    <ErrorBoundary>
      <div className="flex flex-col min-h-screen bg-slate-50">
        <Header />
        <main className="flex-1 container mx-auto px-6 lg:px-8 py-8">
          <ChatContainer />
        </main>
        <Footer />
      </div>
    </ErrorBoundary>
  );
}

export default App;

