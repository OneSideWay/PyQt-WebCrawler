# -*- mode: python -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['E:\\python\\pyqt5-crawler'],
             binaries=[],
             datas=[('qwindowsvistastyle.dll', 'PyQt5/Qt/plugins/styles')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='app',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='prod_cytus.ico')
