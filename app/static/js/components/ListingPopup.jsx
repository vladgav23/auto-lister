// static/js/components/ListingPopup.jsx
const ListingPopup = ({ isOpen, onClose, images, metadata, onConfirm }) => {
    if (!isOpen || !metadata) return null;

    const [editedMetadata, setEditedMetadata] = React.useState({
        title: metadata.title || '',
        description: metadata.description || '',
        price: metadata.estimated_price || 0,
        category: metadata.category || '',
        tags: metadata.tags || []
    });

    // Add new state for tracking submission
    const [isSubmitting, setIsSubmitting] = React.useState(false);

    const handleChange = (field, value) => {
        setEditedMetadata(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleConfirm = () => {
        setIsSubmitting(true);
        onConfirm(editedMetadata);
    };
  
    return (
        <div className="popup-overlay">
            <div className="popup-content">
                <div className="popup-header">
                    <h2>Review Listing</h2>
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
                    <div className="input-group">
                        <label>Title:</label>
                        <input
                            type="text"
                            value={editedMetadata.title}
                            onChange={(e) => handleChange('title', e.target.value)}
                        />
                    </div>

                    <div className="input-group">
                        <label>Price ($):</label>
                        <input
                            type="number"
                            value={editedMetadata.price}
                            onChange={(e) => handleChange('price', e.target.value)}
                        />
                    </div>

                    <div className="input-group">
                        <label>Category:</label>
                        <input
                            type="text"
                            value={editedMetadata.category}
                            onChange={(e) => handleChange('category', e.target.value)}
                        />
                    </div>

                    <div className="input-group">
                        <label>Description:</label>
                        <textarea
                            value={editedMetadata.description}
                            onChange={(e) => handleChange('description', e.target.value)}
                            rows={4}
                        />
                    </div>
                </div>

                <div className="popup-actions">
                    <button 
                        onClick={handleConfirm} 
                        className="confirm-button"
                        disabled={isSubmitting}
                    >
                        {isSubmitting ? 'Creating...' : 'Create Listing'}
                    </button>
                    <button 
                        onClick={onClose} 
                        className="cancel-button"
                        disabled={isSubmitting}
                    >
                        Cancel
                    </button>
                </div>
            </div>
        </div>
    );
};

// Make it available globally
window.ListingPopup = ListingPopup;