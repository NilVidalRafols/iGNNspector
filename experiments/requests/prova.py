# # realitzem request i monitoritzem la descarrega amb una barra
#     response = requests.get(url, stream=True)
#     total_size_in_bytes = int(response.headers.get('content-length', 0))
#     block_size = 1024  # 1 Kibibyte
#     progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
#     with open(path, 'wb') as file:
#         for data in response.iter_content(block_size):
#             progress_bar.update(len(data))
#             file.write(data)
#     progress_bar.close()

#     # comprovem que tot ha anat be
#     if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
#         print("ERROR, something went wrong")
#         err_cap.append(num_cap)
#     else:
#         print()
#         print('El capitol s'ha descarregat correctament')

import requests
x = requests.get('https://sparse.tamu.edu/?per_page=20')

print(x.text)