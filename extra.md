# Kaiwen Luo 
## kluo37@gatech.edu
## Best Accuracy: 76%
----
## What I tried

### 1. My Model
  Basic configuration: (Conv,Pool,Dropout)* n + FC* 1 + Softmax* 1
  
  ```python
  self.seq = nn.Sequential(
  
            nn.Conv2d(self.C, 32, kernel_size, padding =1,padding_mode = "replicate"),
            nn.ReLU(),
            nn.MaxPool2d(2,2),
            nn.Dropout(p=0.2),

            nn.Conv2d(32, 64, kernel_size, padding =1,padding_mode = "replicate"),
            nn.ReLU(),
            nn.MaxPool2d(2,2),
            nn.Dropout(p=0.2),

            nn.Conv2d(64, 128, kernel_size, padding =1,padding_mode = "replicate"),
            nn.ReLU(),
            nn.MaxPool2d(2,2),
            nn.Dropout(p=0.2),

            nn.Conv2d(128, 128,kernel_size , padding =1,padding_mode = "replicate"),
            nn.ReLU(),
            nn.Dropout(p=0.2),

            nn.Flatten(),
            nn.Linear(2048, 128),
            nn.ReLU(),
            nn.Dropout(p=0.2),

            nn.Linear(128, 10),
            nn.Softmax()
            
            )
   ```

2. Pretrained Model - ResNet18
  Don't have enough time to train a complete model.
  Acurracy final achieve 84%
