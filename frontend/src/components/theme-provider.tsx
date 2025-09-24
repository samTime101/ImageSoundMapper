import { createContext, useContext, useEffect } from "react"

type ThemeProviderProps = { children: React.ReactNode }

type ThemeProviderState = { theme: "dark"; setTheme: (t: "dark") => void }

const ThemeProviderContext = createContext<ThemeProviderState>({
  theme: "dark",
  setTheme: () => {},
})

export function ThemeProvider({ children }: ThemeProviderProps) {
  useEffect(() => {
    const root = window.document.documentElement
    if (!root.classList.contains("dark")) {
      root.classList.add("dark")
    }
  }, [])

  return (
    <ThemeProviderContext.Provider value={{ theme: "dark", setTheme: () => {} }}>
      {children}
    </ThemeProviderContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeProviderContext)