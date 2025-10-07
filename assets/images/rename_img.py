import os

def rename_img(source, destinatoin, filename):
    
    try:
        os.rename(
            src=source,
            dst=destinatoin
        )
    except FileExistsError:
        print(f"File {filename} already exists. skipped...")
        
def main(folder):
    full_path = os.path.join(
        os.getcwd(), folder
    )

    df_dir = os.listdir(full_path)
    for ind, dirctory in enumerate(df_dir, start=1):
        df_file = os.listdir(
            os.path.join(
                full_path, dirctory
            )
        )
        if os.path.isdir():
            for i, file in enumerate(df_file, start=1):
                if 'screenshot' not in file.lower():
                    print(f'{file}. Skipped...')
                    continue
                try:
                    os.rename(
                        src=os.path.join(
                            full_path, dirctory, file
                        ),
                        dst=os.path.join(
                            full_path, dirctory, f"{i}.png"
                        )
                    )
                except FileExistsError:
                    print(f"File {i}.png already exists. skipped...")
                    continue
        
        else:
            if 'screenshot' not in file.lower():
                print(f'{file}. Skipped...')
                continue
            try:
                os.rename(
                    src=os.path.join(
                        full_path, dirctory, file
                    ),
                    dst=os.path.join(
                        full_path, dirctory, f"{ind}.png"
                    )
                )
            except FileExistsError:
                print(f"File {ind}.png already exists. skipped...")
                continue

if __name__ == '__main__':
    df_folder = os.listdir(
        os.getcwd()
    )
    while True:
        print('=====================================================================')
        print('pilih folder sesuai nomor urut, untuk di convert nama images nya')
        print('=====================================================================')
        [
            print(f'{i}. {d}') for i, d in enumerate(df_folder, start=1)
        ]
        print('=====================================================================')
        try:
            option = int(input('  => '))
            folder = df_folder[option-1]
            main(folder)
            break
        except ValueError:
            print('harus angka')
        except KeyError:
            print('pilih sesuai nomor urut')