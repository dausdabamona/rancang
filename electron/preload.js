// Preload (sandbox): hanya membuka API kecil ke halaman, tanpa akses Node.
'use strict';
const {contextBridge, ipcRenderer} = require('electron');

contextBridge.exposeInMainWorld('rancangDesktop', {
  awal: () => ipcRenderer.invoke('db:awal'),
  set: (koleksi, id, data) => ipcRenderer.invoke('db:set', koleksi, id, data),
  hapus: (koleksi, id) => ipcRenderer.invoke('db:set', koleksi, id, null),
  setel: data => ipcRenderer.invoke('db:setel', data),
  simpanUnduhan: berkas => ipcRenderer.invoke('unduh:simpan', berkas),
  onUbah: cb => { ipcRenderer.on('db:ubah', (_e, isi) => cb(isi)); },
  onSetel: cb => { ipcRenderer.on('db:setel', (_e, isi) => cb(isi)); }
});
