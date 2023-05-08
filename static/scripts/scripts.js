async function addProduct() {
  const barcode = document.getElementById("barcode").value;
  const url = `https://world.openfoodfacts.org/api/v0/product/${barcode}.json`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    
    const ProductBarcode = barcode;
    const ProductName = data.product.product_name;
    //const productDescription = data.product.generic_name;
    const productImage = data.product.image_url;

    console.log(ProductBarcode, "   ", ProductName, "   ", productImage)

    document.getElementById("barcode").textContent = ProductBarcode;
    document.getElementById("ProductName").textContent = ProductName;
    //document.getElementById("productDescription").textContent = productDescription;
    document.getElementById("product-image").src = productImage;
  } catch (error) {
    console.error(error);
  }
}
