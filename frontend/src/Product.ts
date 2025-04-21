export interface Product {
    _id?: string;
    product_id?: string;
    name: string;
    price: number;
    description: string;
    category: string[];
    brand: string;
    created_at: any;
    updated_at: any
}