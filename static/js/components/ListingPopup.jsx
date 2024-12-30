// static/js/components/ListingPopup.jsx
const ListingPopup = ({ isOpen, onClose, images, metadata }) => {
    if (!isOpen || !metadata) return null;
  
    return (
      <div className="popup-overlay">
        <div className="popup-content">
          <div className="popup-header">
            <h2>{metadata.title}</h2>
            <button onClick={onClose} className="close-button">&times;</button>
          </div>
  
          <div className="image-carousel">
            {images.map((image, index) => (
              <div key={index} className="carousel-item">
                <img src={image} alt={`Product image ${index + 1}`} />
              </div>
            ))}
          </div>
  
          <div className="listing-details">
            <div className="price">${metadata.estimated_price}</div>
            <div className="description">{metadata.description}</div>
          </div>
  
          <button onClick={onClose} className="continue-button">
            Upload listing and continue
          </button>
        </div>
      </div>
    );
  };