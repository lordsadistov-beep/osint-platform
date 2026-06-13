import { ToolWidget } from '../components/ToolWidget'

export function ToolDomain() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Domain Lookup</h1>
      <p className="mb-4 text-sm text-gray-500">WHOIS, DNS, IP информация о домене</p>
      <ToolWidget toolSlug="domain" />
    </div>
  )
}
