BDD100k_originalauthors.pth - Pesi ottenuti dagli autori di TwinLiteNet sull'architettura originale dopo addestramento su BDD100k. Sono stati già rimossi gli elementi non utili all'architettura modificata.

Driving area Segment: Acc(0.903) IOU (0.806) Val_Loss(0.189)
Driving area Segment OFFNET metrics: Acc(0.903) mIOU (0.823) Precision (0.984) Recall (0.817) F1 (0.893) IOU [0] (0.8385819335359626) IoU[1] (0.806)

ORFD_Nocerino.pth - Pesi ottenuto dal pretraining di Nocerino sul dataset ORFD

Driving area Segment: Acc(0.870)    IOU (0.749)    mIOU(0.769)  Val_Loss(0.261)
Driving area Segment OFFNET metrics: Acc(0.870)    Precision (0.938)    Recall(0.788)    F1(0.857)   IOU[0](0.7881991139996277) IoU[1](0.749)

RoverDataset_Nocerino - Pesi ottenuti da Nocerino con finetuning sul RoverDataset (Augmentation SI, Training Set (%) 50 %) dopo aver fatto pretraining su ORFD

Driving area Segment: Acc(0.863) IOU (0.727)
Driving area Segment OFFNET metrics: Acc(0.863) mIOU (0.756) Val_Loss (0.366) Precision (0.979) Recall(0.738) F1(0.841) IOU[0] (0.7854808394500453) IoU[1] (0.726)