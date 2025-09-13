import os

def main():
    full_path = os.getcwd()
    source = [os.path.join(full_path, data) for data in os.listdir()]
    destination = [os.path.join(full_path, str(i+1)+'.png') for i in range(len(source))]
    for src, dst in zip(source, destination):
        try:
            os.rename(
                src=src,
                dst=dst
            )
        except Exception as e:
            print('error:', e)
    
main()