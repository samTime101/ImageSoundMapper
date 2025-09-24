import { Separator } from "@/components/ui/separator"

export function Footer() {
  return (
    <footer className="w-full mt-10">
      <Separator />
      <div className="w-full flex items-center justify-center py-6 px-4">
        <p className="text-sm text-muted-foreground text-center">
          &copy; {new Date().getFullYear()} SamTime101. All rights reserved.
        </p>
      </div>
    </footer>
  )
}
