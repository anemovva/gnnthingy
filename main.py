# from torch_geometric.data import Data
from torch_geometric.data import DataLoader
# from torch_geometric.datasets import Planetoid
import torch_geometric.datasets.citation_full as citation_full
import torch
# import dgl

import torch.nn as nn
from gat import GAT


def main() -> None:
    """Main function for training GAT on the CORA dataset.
    """
    # Get CORA dataset from DGL

   # Create DataLoader
    # open ./data/cora/cora.content
    # open ./data/cora/cora.cites
    # Create DataLoader


    dataset = citation_full.CitationFull(root='./data/CoraML', name='cora_ML')

    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)



    # Create model, try setting to cuda, cpu if not available
    device = torch.device('cpu')
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = GAT(dataset.num_features, dataset.num_classes).to(device)

    # Define loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    print("Training")

    # Training loop

    initial = 0
    best = 100000000000


    # Look at data
    for data in dataloader:
        freq = {}
        for i in data.y:
            if i.item() in freq:
                freq[i.item()] += 1
            else:
                freq[i.item()] = 1
        print(freq)

    for epoch in range(1000):
        total_loss = 0
        for data in dataloader:
            # data = data.to(device)
            # Convert targets to float
            optimizer.zero_grad()
            output = model.forward(data)

            loss = criterion(output, data.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        if total_loss < best:
            best = total_loss
        if initial == 0:
            initial = total_loss
        print(f"Epoch {epoch+1}: Loss = {total_loss} (Initial = {initial}, Best = {best})")
    return

main()
