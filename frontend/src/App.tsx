import Converter from "@/components/converter"
import { Footer } from "@/components/footer"

export default function App() {
  return (
    // Got some super duper colors from https://ui.shadcn.com/colors
    <div className="min-h-screen flex flex-col bg-stone-950">
      <main className="flex-1 flex items-center justify-center p-4 md:p-6">
        <div className="w-full max-w-2xl">
          <Converter />
        </div>
      </main>
      <Footer />
    </div>
  )
}
