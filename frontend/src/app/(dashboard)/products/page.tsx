'use client';

import { useContentItems } from '@/hooks/use-content';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ShoppingCart, Loader2 } from 'lucide-react';

import { Skeleton } from '@/components/ui';

export default function ProductsPage() {
  const { data: products, isLoading } = useContentItems('product');

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <Skeleton className="h-8 w-48 mb-2" />
          <Skeleton className="h-4 w-64" />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
            <Card key={i} className="flex flex-col">
              <Skeleton className="aspect-video w-full rounded-t-lg" />
              <CardHeader>
                <Skeleton className="h-6 w-3/4" />
              </CardHeader>
              <CardContent className="flex-1 space-y-2">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-2/3" />
                <div className="mt-4 flex items-baseline gap-2">
                  <Skeleton className="h-8 w-24" />
                </div>
              </CardContent>
              <CardFooter>
                <Skeleton className="h-10 w-full" />
              </CardFooter>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Products</h1>
        <p className="text-gray-500">Browse our catalog</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {products?.map((product) => (
          <Card key={product.id} className="flex flex-col">
            {product.fields.image && (
              <div className="aspect-video w-full overflow-hidden rounded-t-lg bg-gray-100 relative">
                <img
                  src={product.fields.image.url || '/placeholder-product.jpg'}
                  alt={product.fields.title}
                  className="w-full h-full object-cover transition-transform hover:scale-105"
                />
              </div>
            )}
            <CardHeader>
              <CardTitle className="line-clamp-1">{product.fields.title}</CardTitle>
            </CardHeader>
            <CardContent className="flex-1">
              <p className="text-sm text-gray-500 line-clamp-3">
                {product.fields.description}
              </p>
              <div className="mt-4 flex items-baseline gap-2">
                <span className="text-2xl font-bold text-gray-900">
                  ${product.fields.price}
                </span>
                {product.fields.compare_at_price && (
                  <span className="text-sm text-gray-500 line-through">
                    ${product.fields.compare_at_price}
                  </span>
                )}
              </div>
            </CardContent>
            <CardFooter>
              <Button className="w-full">
                <ShoppingCart className="mr-2 h-4 w-4" />
                Add to Cart
              </Button>
            </CardFooter>
          </Card>
        ))}

        {(!products || products.length === 0) && (
          <div className="col-span-full text-center py-12">
            <p className="text-gray-500">No products found.</p>
          </div>
        )}
      </div>
    </div>
  );
}
