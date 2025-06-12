import pandas as pd
import torch
from PIL import ImageFile
from torch.utils.data import Dataset
from config import types


ImageFile.LOAD_TRUNCATED_IMAGES = True


class SDNDataset(Dataset):
    def __init__(
            self,
            csv_file,
            transform=None,
    ):
        super(SDNDataset, self).__init__()
        self.annotations = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        label = self.annotations.iloc[index, -1]
        data = self.annotations.iloc[index, :-1]
        label = types.index(label)
        # if self.transform:NUM_CLASSES
        #     data = self.transform(data=data)["data"]
        #     label = self.transform(label=label)["label"]
        label = torch.tensor(label, dtype=torch.int64)
        data = torch.tensor(data, dtype=torch.float32)
        # data = data.unsqueeze(dim=0)
        return data, label
