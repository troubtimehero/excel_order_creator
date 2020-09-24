# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['order_creator_service.py'],
             pathex=['D:\\Projects\\Pro_py\\excel_order_creator'],
             binaries=[],
             datas=[
                (r'app\static', r'app\static'),
                (r'app\templates', r'app\templates'),
                (r'config.json', r'config.json'),
                (r'settings_produce.json', r'settings_produce.json'),
                (r'settings_sell.json', r'settings_sell.json'),
                (r'data.sqlite', r'data.sqlite')
			 ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='order_creator_service',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
