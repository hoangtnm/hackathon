import os

import cv2
from config import CHECKPOINT_PATH
from config import CLASSES
from utils import get_device
from utils import get_net
from utils import get_result

if __name__ == '__main__':
    device = get_device()
    num_classes = len(CLASSES)

    net = get_net(model_name='mobilenet_v2', mode='inference', device=device,
                  pretrained=False, num_classes=num_classes, checkpoint_path=CHECKPOINT_PATH)

    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(os.path.join('videos', 'video_03.mp4'))

    while True:
        _, frame = cap.read()
        result = get_result(frame, CLASSES, net, device)
        print(f'Result: {result}')

        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
