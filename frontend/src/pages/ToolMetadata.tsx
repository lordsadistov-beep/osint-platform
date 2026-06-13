import { ToolWidget } from '../components/ToolWidget'

export function ToolMetadata() {
  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold text-gray-100">Metadata Extractor</h1>
      <p className="mb-4 text-sm text-gray-500">Извлечение EXIF/metadata из файлов</p>
      <ToolWidget toolSlug="metadata" />
    </div>
  )
}
