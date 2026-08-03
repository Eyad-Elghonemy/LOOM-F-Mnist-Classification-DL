import numpy as np
from PIL import Image
from io import BytesIO
from .config import MODEL, CLASS_NAMES
from .logger import log_prediction


def classify_fmnist(image_bytes: bytes):
    try:
        img = Image.open(BytesIO(image_bytes))
        if img.mode != 'L':
            img = img.convert('L')

        img = img.resize((28, 28))

        img_array = np.array(img)

        img_array = img_array.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # الشكل هيبقي (1, 28, 28)

        prediction = MODEL.predict(img_array, verbose=0)
        predicted_class = np.argmax(prediction, axis=-1)[0]
        predicted_name = CLASS_NAMES[predicted_class]
        confidence = float(prediction[0][predicted_class] * 100)

        # Log the successful prediction
        log_prediction(
            success=True,
            class_index=int(predicted_class),
            predicted_class=predicted_name,
            confidence=confidence,
        )

        return {
            'class_index': int(predicted_class),
            'class_name': predicted_name,
            'confidence': confidence
        }

    except Exception as e:
        # Log the failed attempt too (no class/confidence available)
        log_prediction(success=False)
        raise ValueError(f'image Processing Failed: {str(e)}')