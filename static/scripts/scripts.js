async function addProduct() {
  const barcode = document.getElementById("barcode").value;
  const url = `https://world.openfoodfacts.org/api/v0/product/${barcode}.json`;

  try {
    const response = await fetch(url);
    const data = await response.json();
    
    const ProductBarcode = barcode;
    const ProductName = data.product.product_name;
    const productImage = data.product.image_url;

    console.log(ProductBarcode, "   ", ProductName, "   ", productImage)

    document.getElementById("barcode").textContent = ProductBarcode;
    document.getElementById("name").textContent = ProductName;
    document.getElementById("imgurl_pic").src = productImage;
    document.getElementById("imgurl").textContent = productImage;
    console.log(productImage)
  } catch (error) {
    console.error(error);
  }
}


function increase() {
  document.getElementById('quantity').stepUp();
}

function decrease() {
  document.getElementById('quantity').stepDown();
}

