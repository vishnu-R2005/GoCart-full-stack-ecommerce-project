export function ProductCardSkeleton() {
  return (
    <div className="card p-4 animate-pulse">
      <div className="bg-gray-200 dark:bg-gray-700 h-48 rounded-lg mb-4" />
      <div className="bg-gray-200 dark:bg-gray-700 h-4 rounded w-3/4 mb-2" />
      <div className="bg-gray-200 dark:bg-gray-700 h-4 rounded w-1/2" />
    </div>
  )
}

export function ProductGridSkeleton({ count = 8 }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <ProductCardSkeleton key={i} />
      ))}
    </div>
  )
}
