const CameraApp = {
    handleUploadAndNext: async (capturedPhotos, showStatus, updateThumbnails, updatePhotoCount) => {
        if (capturedPhotos.length === 0) {
            showStatus('Take photos first');
            return;
        }

        showStatus('Generating listing details...', 999999);

        try {
            const metadataResponse = await fetch('/generate-metadata', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    images: capturedPhotos
                }),
            });

            const metadataResult = await metadataResponse.json();

            if (!metadataResult.success) {
                throw new Error(metadataResult.message);
            }

            const croppedImages = metadataResult.cropped_images;

            const popupRoot = document.getElementById('popup-root');
            
            ReactDOM.render(
                <ListingPopup
                    isOpen={true}
                    images={croppedImages}
                    metadata={metadataResult.metadata}
                    onClose={() => {
                        ReactDOM.unmountComponentAtNode(popupRoot);
                        status.style.display = 'none';
                    }}
                    onConfirm={async (editedMetadata) => {
                        showStatus('Creating Shopify listing...', 999999);
                        try {
                            const finalMetadata = {
                                ...editedMetadata,
                                tags: editedMetadata.tags || [],
                                price: editedMetadata.price || 0,
                            };

                            const createResponse = await fetch('/create-listing', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    images: croppedImages,
                                    metadata: finalMetadata
                                }),
                            });

                            const createResult = await createResponse.json();

                            if (createResult.success) {
                                showStatus('Listing created successfully!');
                                capturedPhotos.length = 0;
                                updateThumbnails();
                                updatePhotoCount();
                                ReactDOM.unmountComponentAtNode(popupRoot);
                            } else {
                                throw new Error(createResult.message);
                            }
                        } catch (error) {
                            showStatus('Error creating listing: ' + error.message);
                        }
                    }}
                />,
                popupRoot
            );

        } catch (error) {
            showStatus('Error: ' + error.message);
        }
    }
};

window.CameraApp = CameraApp; 