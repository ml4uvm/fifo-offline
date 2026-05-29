# offline-ml
Coverage-driven test case prioritization using ML (offline phase)


Terminal-1:
````
cd ~/ml4uvm/fifo-offline/tb/tests
gedit fifo_test.py 
change ml to baseline and vice versa

cd ~/ml4uvm/offline-ml/ml:
gedit cluster_tests.py 
chnage cluster accordingly
````

Terminal-2:
````
cd ~/ml4uvm/offline-ml
make clean
make

cd ml
python3 train_model.py
python3 cluster_test.py

````


