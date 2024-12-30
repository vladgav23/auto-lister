// static/js/components/ListingPopup.jsx
const ListingPopup = ({ isOpen, onClose, images, shopifyProduct }) => {
    if (!isOpen || !shopifyProduct) return null;
  
    return (
      <div className="popup-overlay">
        <div className="popup-content">
          <div className="popup-header">
            <h2>{shopifyProduct.title}</h2>
            <button onClick={onClose} className="close-button">&times;</button>
          </div>
  
          <div className="image-carousel">
            {shopifyProduct.images.map((image, index) => (
              <div key={index} className="carousel-item">
                <img src={image} alt={`Product image ${index + 1}`} />
              </div>
            ))}
          </div>
  
          <div className="listing-details">
            <div className="price">${shopifyProduct.price}</div>
            <div className="description">{shopifyProduct.description}</div>
            <div className="category">Category: {shopifyProduct.category}</div>
            <div className="url">
              <a href={shopifyProduct.url} target="_blank" rel="noopener noreferrer">
                View on Shopify
              </a>
            </div>
          </div>
  
          <button onClick={onClose} className="continue-button">
            Continue to next item
          </button>
        </div>
      </div>
    );
  };