#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : packing_app.py.py
# @Author   : jade
# @Date     : 2021/11/27 14:25
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
from jade import AppRunPath, LogoPath
from jade.jade_tools import CreateSavePath, GetTimeStamp, GetLastDir, GetYear, getOperationSystem, GetPreviousDir,zip_file
from jade.jade_progress_bar import ProgressBar
import os
import shutil
import platform
import subprocess
import uuid
import re

def str_to_bool(str):
    if str == "False":
        return False
    elif str == "True":
        return True
    else:
        return False


def copy_build(args, save_path):
    if getOperationSystem() == "Windows":
        save_path = save_path
    else:
        save_path = "/mnt/" + save_path[0].lower() + save_path.replace("\\", "//")[2:]

    for file_name in os.listdir(args.lib_path):
        shutil.copy(os.path.join(args.lib_path, file_name),
                    os.path.join(save_path, getOperationSystem(), args.lib_path))


def ui_to_py(trans=False):
    view_path = "view"
    view_file_list = os.listdir(view_path)
    progressBar = ProgressBar(len(view_file_list))
    for view_name in view_file_list:
        if "ui" in view_name:
            view_file = os.path.join(view_path, view_name)
            os.system("pyuic5 -o {}.py {}".format(view_file.split(".ui")[0], view_file))
            if trans:
                CreateSavePath("translator_ts_tmp")
                os.system("pylupdate5 {}.py -ts translator_ts_tmp/{}.ts".format(view_file.split(".ui")[0],
                                                                                view_name.split(".ui")[0]))
        progressBar.update()


def get_import_content(f1, src_import, content, import_list):
    prefix_list = content.split("from")[1].split("import")[0].split(".")[:-1]
    prefix = ""
    edit = False
    if len(prefix_list) > 0:
        for text in prefix_list:
            prefix = prefix + text + "."
    if src_import == prefix.strip():
        new_content = content.split(src_import)[0] + \
                      content.split(src_import)[1]
        f1.write((new_content + '\n').encode("utf-8"))
        if new_content not in import_list and "#" not in new_content and \
                new_content[
                    0] != " ":
            import_list.append(new_content)
        edit = True
    return edit


def writePyContent(args,src_path,new_src_path,src_path_list,src_import_list,import_list):
    for file_name in os.listdir(src_path):
        if os.path.isfile(os.path.join(src_path, file_name)):
            file_name_suffix = re.search(r"\.(\w+)$", file_name).group(1)
            if file_name_suffix == "py":
                if "__init__.py" == file_name :
                    if src_path not in src_path_list :
                        with open(os.path.join(new_src_path, GetLastDir(src_path)) + ".py", "wb") as f1:
                            with open(os.path.join(src_path, file_name), "rb") as f:
                                try:
                                    content_list = str(f.read(), encoding="utf-8").split("\n")
                                except:
                                    pass
                                for content in content_list:
                                    if "import" in content or ("from" in content and "import" in content):
                                        edit = False
                                        for src_import in src_import_list:
                                            if "from" in content:
                                                prefix_list = content.split("from")[1].split("import")[0].split(".")[
                                                              :-1]
                                                prefix = ""
                                                if len(prefix_list) > 0:
                                                    for text in prefix_list:
                                                        prefix = prefix + text + "."
                                                if src_import in prefix.strip():
                                                    f1.write(
                                                        (content.replace(prefix.strip(), "") + '\n').encode("utf-8"))
                                                    edit = True
                                                    break
                                        if edit is False:
                                            f1.write((content + '\n').encode("utf-8"))
                                    elif "JadeLog = JadeLogging" in content:
                                        if str_to_bool(args.use_jade_log):
                                            update_log = "\n    JadeLog.INFO('{}-更新时间为:{}',True)\r".format(
                                                args.name + "V" + args.app_version, GetTimeStamp(), True)
                                            f1.write((content + update_log).encode("utf-8"))
                                        else:
                                            f1.write((content).encode("utf-8"))
                                    else:
                                        f1.write((content + "\n").encode("utf-8"))
                elif file_name != "samplesMain.py":
                    with open(os.path.join(new_src_path, file_name), "wb") as f1:
                        with open(os.path.join(src_path, file_name), "rb") as f:
                            try:
                                content_list = str(f.read(), encoding="utf-8").split("\n")
                            except:
                                pass
                            for content in content_list:
                                if "import" in content or ("from" in content and "import" in content):
                                    edit = False
                                    for src_import in src_import_list:
                                        if "from" in content:
                                            prefix_list = content.split("from")[1].split("import")[0].split(".")[:-1]
                                            prefix = ""
                                            if len(prefix_list) > 0:
                                                for text in prefix_list:
                                                    prefix = prefix + text + "."
                                            if src_import == prefix.strip():
                                                new_content = content.split(src_import)[0] + \
                                                              content.split(src_import)[1]
                                                f1.write((new_content + '\n').encode("utf-8"))
                                                if new_content not in import_list and "#" not in new_content and \
                                                        new_content[
                                                            0] != " ":
                                                    import_list.append(new_content)
                                                edit = True
                                                break
                                    if edit is False:
                                        f1.write((content + '\n').encode("utf-8"))
                                        if content not in import_list and "#" not in content and content[0] != " ":
                                            import_list.append(content)
                                elif "JadeLog = JadeLogging" in content:
                                    if str_to_bool(args.use_jade_log):
                                        update_log = "\n    JadeLog.INFO('{}-更新时间为:{}',True)\r".format(
                                            args.name + "V" + args.app_version, GetTimeStamp(), True)
                                        f1.write((content + update_log).encode("utf-8"))
                                    else:
                                        f1.write((content).encode("utf-8"))
                                else:
                                    f1.write((content + "\n").encode("utf-8"))
                else:
                    with open(os.path.join(new_src_path, file_name), "wb") as f1:
                        with open(os.path.join(src_path, file_name), "rb") as f:
                            content_list = str(f.read(), encoding="utf-8").split("\n")
                            for content in content_list:
                                if "import" in content or ("from" in content and "import" in content):
                                    edit = False
                                    for src_import in src_import_list:
                                        if "from" in content:
                                            prefix_list = content.split("from")[1].split("import")[0].split(".")[:-1]
                                            prefix = ""
                                            if len(prefix_list) > 0:
                                                for text in prefix_list:
                                                    prefix = prefix + text + "."
                                            if src_import == prefix.strip():
                                                new_content = content.split(src_import)[0] + \
                                                              content.split(src_import)[1]
                                                f1.write((new_content + '\n').encode("utf-8"))
                                                if new_content not in import_list and "#" not in new_content and \
                                                        new_content[
                                                            0] != " ":
                                                    import_list.append(new_content)
                                                edit = True
                                                break

                                    if edit is False:
                                        f1.write((content + '\n').encode("utf-8"))
                                        if content not in import_list and "#" not in content and content[0] != " ":
                                            import_list.append(content)
                                elif "def main():" in content:
                                    if str_to_bool(args.use_jade_log) is False:
                                        update_log = "print('#'*20+ '{}-更新时间为:{}' +'#'*20)\r".format(
                                            args.name + "V" + args.app_version,
                                            GetTimeStamp())
                                        f1.write((update_log + content).encode("utf-8"))
                                    else:
                                        f1.write((content + "\n").encode("utf-8"))
                                else:
                                    f1.write((content + '\n').encode("utf-8"))
        else:
            if os.path.isdir( os.path.join(src_path, file_name)) and "pycache" not in file_name:
                writePyContent(args, os.path.join(src_path, file_name), new_src_path,src_path_list,src_import_list, import_list)

def copyPy(args):
    new_src_path = CreateSavePath("new_src")
    try:
        if str_to_bool(args.is_qt) is False:
            src_path_list = ["src"]
            src_import_list = ["src."]
        else:
            src_path_list = ["src", "view", "view/customView", "controller"]
            src_import_list = ["src.", "view.", "view.customView.", "controller."]
    except:
        src_path_list = ["src"]
        src_import_list = ["src."]
    import_list = []
    for src_path in src_path_list:
        writePyContent(args,src_path,new_src_path,src_path_list,src_import_list,import_list)
    if args.app_version:
        with open("new_src/samplesVersion.py","wb") as f:
            f.write('#!/usr/bin/env python\n'
                    '# -*- coding: utf-8 -*-\n'
                    '# @File     : __version__.py\n'
                    '# @Author   : jade\n'
                    '# @Date     : 2023/3/7 16:19\n'
                    '# @Email    : jadehh@1ive.com\n'
                    '# @Software : Samples\n'
                    '# @Desc     :\n'
                    'app_version = "{}"\n'
                    'log_level = "DEBUG"'.format(args.app_version).encode("utf-8"))
    return import_list


def writePy(args):
    or_import_list = copyPy(args)
    import_list = []
    for import_content in or_import_list:
        try:
            content = import_content.split("import")[1].strip()
            if content in args.remove_import_list:
                pass
            else:
                import_list.append(import_content)
        except:
            import_list = or_import_list
    app_name = get_app_name(args)
    with open("{}.py".format(app_name), "wb") as f:
        try:
            if args.head_str:
                if "\\n" in args.head_str:
                    new_head_str = ""
                    for head_str in args.head_str.split("\\n"):
                        new_head_str = new_head_str + head_str + "\n"
                    args.head_str = new_head_str
                f.write(args.head_str.encode("utf-8"))
        except:
            pass
        f.write("import sys\n"
                "import os\n"
                "if getattr(sys, 'frozen', False): #是否Bundle Resource\n"
                "    base_path = sys._MEIPASS\n"
                "else:\n"
                "    base_path = os.path.abspath('.')\n"
                "sys.path.append('new_src')\n"
                "sys.path.append('{}')\n"
                "sys.path.append(os.path.join(base_path,'build/encryption'))\n".format(args.lib_path).encode("utf-8"))
        try:
            for extra_sys_path in str_to_list(args.extra_sys_str):
                f.write(("sys.path.append" + "('" + extra_sys_path + "')" + "\n").encode("utf-8"))
        except:
            pass

        for import_src in import_list:
            f.write(import_src.encode("utf-8") + "\n".encode("utf-8"))

        try:
            if args.main:
                if os.path.exists(args.main):
                    if args.main.endswith(".py"):
                        with open(args.main, "rb") as f2:
                            for content in f2.readlines():
                                content_str = str(content, encoding="utf-8")
                                if content_str[0] == "#":
                                    pass
                                elif "from src." in content_str:
                                    f.write(content_str.replace("src.", "").encode("utf-8"))
                                else:
                                    f.write(content)
                else:
                    f.write(args.main.encode("utf-8"))
            else:
                f.write("from samplesMain import main\n"
                        "if __name__ == '__main__':\n"
                        "    main()\n".encode("utf-8"))
        except Exception as e:
            f.write("from samplesMain import main\n"
                    "if __name__ == '__main__':\n"
                    "    main()\n".encode("utf-8"))


def get_app_name(args):
    return args.app_name


def write_version_info(args):
    with open("file_verison_info.txt", "wb") as f:
        version_str = ""
        for version_word in args.app_version.split("."):
            version_str = version_str + version_word + ","
        version_str = version_str[:-1]
        origanl_app_name = ""
        app_version = ""
        if len(args.app_version.split(".")) < 3:
            raise "请确认App Version参数是否按照规范,1.0.0或1.0.0.0"
        if len(args.app_version.split(".")) == 3:
            app_version = args.app_version
            version_str = version_str + ",1"
        if len(args.app_version.split(".")) == 4:
            app_version = args.app_version[:-2]
        if getOperationSystem() == "Windows":
            origanl_app_name = args.app_name + ".exe"
        else:
            origanl_app_name = args.app_name + "v" + args.app_version
        f.write("# UTF-8\n"
                "#\n"
                "# For more details about fixed file info 'ffi' see:\n"
                "# http://msdn.microsoft.com/en-us/library/ms646997.aspx\n"
                "VSVersionInfo(\n"
                "   ffi=FixedFileInfo(\n"
                "# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)\n"
                "# Set not needed items to zero 0.\n"
                "filevers=({}),  # 文件版本\n"
                "prodvers=({}),\n"
                "# Contains a bitmask that specifies the valid bits 'flags'r\n"
                "mask=0x3f,\n"
                "# Contains a bitmask that specifies the Boolean attributes of the file.\n"
                "flags=0x0,\n"
                "# The operating system for which this file was designed.\n"
                "# 0x4 - NT and there is no need to change it.\n"
                "# OS=0x4,\n"
                "# The general type of file.\n"
                "# 0x1 - the file is an application.\n"
                "fileType=0x1, # 类型\n"
                "# The function of the file.\n"
                "# 0x0 - the function is not defined for this fileType\n"
                "subtype=0x0,\n"
                "# Creation date and time stamp.\n"
                "date=(0, 0)\n"
                "),\n"
                "kids=[\n"
                "StringFileInfo(\n"
                "[\n"
                "StringTable(\n"
                "u'040904B0',\n"
                "[StringStruct(u'CompanyName', u'南京三宝科技有限公司'),\n"
                "StringStruct(u'FileDescription', u'{}'),    # 文件说明\n"
                "StringStruct(u'FileVersion', u'{}'),\n"
                "StringStruct(u'InternalName', u'Git'),\n"
                " StringStruct(u'LegalCopyright', u'Copyright (C) 2019-{} Samples, Inc.'), #版权\n"
                "StringStruct(u'OriginalFilename', u'{}'), #原始文件名\n"
                "StringStruct(u'ProductName', u'{}'),      #产品名称\n"
                "StringStruct(u'ProductVersion', u'{}')])    #产品版本\n"
                "]),\n"
                "VarFileInfo([VarStruct(u'Translation', [2052, 1200])]) # 语言\n"
                "]\n"
                ")\n".format(version_str, version_str, args.name, app_version, GetYear(), origanl_app_name,
                             get_app_name(args), app_version).encode("utf-8"))


def recursion_dir_all_file(path):
    '''
    :param path: 文件夹目录
    '''
    file_list = []
    for dir_path, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(dir_path, file)
            if "\\" in file_path:
                file_path = file_path.replace('\\', '/')
            file_list.append(file_path)
        for dir in dirs:
            file_list.extend(recursion_dir_all_file(os.path.join(dir_path, dir)))
    return file_list


def get_file_data_str(file_path, save_path):
    data_str = ""
    file_list = recursion_dir_all_file(file_path)
    for (i, file) in enumerate(file_list):
        if i == len(file_list) - 1:
            data_str = data_str + "('{}','{}')".format(file, GetPreviousDir(save_path + file.split(file_path)[-1]))
        else:
            data_str = data_str + "('{}','{}')".format(file,
                                                       GetPreviousDir(save_path + file.split(file_path)[-1])) + ","

    return data_str


def writeSpec(args):
    data_str = "datas=["
    if args.lib_path:
        pass
    else:
        file_list = os.listdir("build/encryption")
        for i in range(len(file_list)):
            file_path = "build/encryption/{}".format(file_list[i])
            file_path_str = ("'{}'".format(file_path))
            file_path_list_str = "({},'.')".format(file_path_str)
            data_str = data_str + file_path_list_str + ","

    extra_path_list = args.extra_path_list
    if len(extra_path_list) == 0:
        data_str = data_str + "]"
    else:
        for i in range(len(extra_path_list)):
            if type(extra_path_list[i]) == tuple:
                bin_path = extra_path_list[i][0]
                save_path = extra_path_list[i][1]
            else:
                bin_path = extra_path_list[i]
                save_path = extra_path_list[i]
            if os.path.isdir(bin_path):
                if type(extra_path_list[i]) == tuple:
                    if i == len(extra_path_list) - 1:
                        data_str = data_str + get_file_data_str(bin_path, save_path) + "]"
                    else:
                        data_str = data_str + get_file_data_str(bin_path, save_path) + ","
                else:
                    file_path = bin_path
                    file_path_str = ("'{}'".format(file_path))
                    file_path_list_str = "({},'{}')".format(file_path_str, save_path)
                    if i == len(extra_path_list) - 1:
                        data_str = data_str + file_path_list_str + "]"
                    else:
                        data_str = data_str + file_path_list_str + ","
            else:
                file_path = bin_path
                file_path_str = ("'{}'".format(file_path))
                file_path_list_str = "({},'{}')".format(file_path_str, save_path)
                if i == len(extra_path_list) - 1:
                    data_str = data_str + file_path_list_str + "]"
                else:
                    data_str = data_str + file_path_list_str + ","

    binaries_str = "binaries=["
    if os.path.exists("icons"):
        icon_list = os.listdir("icons")
        for i in range(len(icon_list)):
            if i == len(icon_list) - 1:
                binaries_str = binaries_str + "('icons/{}','{}')]".format(icon_list[i], "icons")
            else:
                binaries_str = binaries_str + "('icons/{}','{}'),".format(icon_list[i], "icons")
    else:
        binaries_str = binaries_str + "]"

    icon_path = "icons/app_logo.ico"
    if os.path.exists(icon_path):
        pass
    else:
        icon_path = ""
    exclude_files_str = ""
    try:
        exclude_files_list = str_to_list(args.exclude_files)
        if len(exclude_files_list) > 0:
            exclude_files_str = exclude_files_str + "a.binaries = a.binaries - TOC([\n"
        for exclude_file in exclude_files_list:
            exclude_files_str = exclude_files_str + "\t('{}',None, None),\n".format(exclude_file)
        if len(exclude_files_list) > 0:
            exclude_files_str = exclude_files_str + "])\n"
    except:
        pass
    if getOperationSystem() == "Darwin":
        with open("{}.spec".format(get_app_name(args)), "wb") as f:
            f.write(("# -*- mode: python ; coding: utf-8 -*-\n\n\n"
                     "block_cipher = None\n\n\n"
                     "a = Analysis(['{}.py'],\n"
                     "\t\t\tpathex=[],\n"
                     "\t\t\t{},\n"
                     "\t\t\t{},\n"
                     "\t\t\thiddenimports=[],\n"
                     "\t\t\thookspath=[],\n"
                     "\t\t\thooksconfig=[],\n"
                     "\t\t\truntime_hooks=[],\n"
                     "\t\t\texcludes=[],\n"
                     "\t\t\twin_no_prefer_redirects=False,\n"
                     "\t\t\twin_private_assemblies=False,\n"
                     "\t\t\tcipher=block_cipher,\n"
                     "\t\t\tnoarchive=False)\n"
                     "{}\n"
                     "pyz = PYZ(a.pure, a.zipped_data,\n"
                     "\t\t\tcipher=block_cipher)\n\n"
                     "exe = EXE(pyz,\n"
                     "\t\t\ta.scripts,\n"
                     "\t\t\ta.binaries,\n"
                     "\t\t\ta.zipfiles,\n"
                     "\t\t\ta.datas,  \n"
                     "\t\t\t[],\n"
                     "\t\t\tname='{}',\n"
                     "\t\t\tdebug=False,\n"
                     "\t\t\tbootloader_ignore_signals=False,\n"
                     "\t\t\tupx=True,\n"
                     "\t\t\tupx_exclude=[],\n"
                     "\t\t\truntime_tmpdir=None,\n"
                     "\t\t\tconsole=False,\n"
                     "\t\t\tdisable_windowed_traceback=False,\n"
                     "\t\t\ttarget_arch=None,\n"
                     "\t\t\tcodesign_identity=None,\n"
                     "\t\t\tentitlements_file=None , icon='{}')\n"
                     "app = BUNDLE(exe,\n"
                     "\t\t\tname='{}.app',\n"
                     "\t\t\ticon='{}',\n"
                     "\t\t\tbundle_identifier=None,\n"
                     "\t\t\tinfo_plist = ".format(get_app_name(args),
                                                  binaries_str,
                                                  data_str,
                                                  exclude_files_str,
                                                  get_app_name(args), icon_path, get_app_name(args), icon_path) +
                     "{\n\t\t\t\t\t\t\t'NSHighResolutionCapable':'True','CFBundleShortVersionString':" + "'{}'".format(
                        args.app_version[:-2])
                     + "\n\t\t\t\t\t\t\t})\n").encode('utf-8')
                    )
    else:
        if str_to_bool(args.full) is False:
            with open("{}.spec".format(get_app_name(args)), "wb") as f:
                f.write("block_cipher = None\n"
                        "a = Analysis(['{}.py'],\n"
                        "             pathex=[''],\n"
                        "             {},\n"
                        "             {},\n"
                        "             hiddenimports=[],\n"
                        "             hookspath=[],\n"
                        "             runtime_hooks=[],\n"
                        "             excludes=[],\n"
                        "             win_no_prefer_redirects=False,\n"
                        "             win_private_assemblies=False,\n"
                        "             cipher=block_cipher,\n"
                        "             noarchive=False)\n"
                        "{}"
                        "pyz = PYZ(a.pure, a.zipped_data,\n"
                        "             cipher=block_cipher)\n"
                        "exe2 = EXE(pyz,\n"
                        "          a.scripts,\n"
                        "          [],\n"
                        "          exclude_binaries=True,\n"
                        "          name='{}',\n"
                        "          debug=False,\n"
                        "          bootloader_ignore_signals=False,\n"
                        "          strip=False,\n"
                        "          upx=True,\n"
                        "          console={},\n"
                        "          icon='{}',\n"
                        "          version='file_verison_info.txt')\n"
                        "coll = COLLECT(exe2,\n"
                        "          a.binaries,\n"
                        "          a.zipfiles,\n"
                        "          a.datas,\n"
                        "          strip=False,\n"
                        "          upx=True,\n"
                        "          upx_exclude=[],\n"
                        "          name='{}')\n".format(get_app_name(args),
                                                        binaries_str,
                                                        data_str,
                                                        exclude_files_str,
                                                        get_app_name(args),
                                                        args.console, icon_path,
                                                        get_app_name(args)).encode("utf-8"))
        else:
            with open("{}.spec".format(get_app_name(args)), "wb") as f:
                f.write("block_cipher = None\n"
                        "a = Analysis(['{}.py'],\n"
                        "             pathex=[''],\n"
                        "             {},\n"
                        "             {},\n"
                        "             hiddenimports=[],\n"
                        "             hookspath=[],\n"
                        "             runtime_hooks=[],\n"
                        "             excludes=[],\n"
                        "             win_no_prefer_redirects=False,\n"
                        "             win_private_assemblies=False,\n"
                        "             cipher=block_cipher,\n"
                        "             noarchive=False)\n"
                        "{}"
                        "pyz = PYZ(a.pure, a.zipped_data,\n"
                        "             cipher=block_cipher)\n"
                        "exe1 = EXE(pyz,\n"
                        "          a.scripts,\n"
                        "          a.binaries,\n"
                        "          a.zipfiles,\n"
                        "          a.datas,\n"
                        "          [],\n"
                        "          name='{}',\n"
                        "          debug=False,\n"
                        "          bootloader_ignore_signals=False,\n"
                        "          strip=False,\n"
                        "          upx=True,\n"
                        "          upx_exclude=[],\n"
                        "          runtime_tmpdir=None,\n"
                        "          console={},\n"
                        "          icon='{}',\n"
                        "          version='file_verison_info.txt')\n"
                    .format(get_app_name(args),
                            binaries_str,
                            data_str,
                            exclude_files_str,
                            get_app_name(args), args.console,
                            icon_path).encode(
                    "utf-8"))


def str_to_list(str):
    str_list = []
    for z in str.split(","):
        if z:
            str_list.append(z)
    return str_list


def build(args):
    writePy(args)
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    os.mkdir("build/")
    if args.lib_path:
        ep_build_path = args.lib_path
    else:
        ep_build_path = "build/encryption/"

    if os.path.exists(ep_build_path):
        shutil.rmtree(ep_build_path)
    os.mkdir(ep_build_path)
    file_list = os.listdir("new_src")
    bin_suffix = ""

    if getOperationSystem() == "Windows":
        bin_suffix = ".exe"
    if getOperationSystem() == "Windows":
        lib_suffix = "pyd"
    else:
        lib_suffix = "so"

    specify_files = str_to_list(args.specify_files)

    if len(specify_files) > 0:
        progressBar = ProgressBar(len(specify_files))
    else:
        progressBar = ProgressBar(len(file_list))
    scripts_path = ""
    try:
        if args.scripts_path:
            scripts_path = args.scripts_path + "/"
    except:
        pass
    need_to_build_file_list = []
    for file_name in file_list:
        if len(specify_files) > 0:
            if file_name in specify_files:
                cmd_str = "{}easycython {}/{}".format(scripts_path, "new_src", file_name)
                result = subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                progressBar.update()
                need_to_build_file_list.append(file_name)
            else:
                pass
        else:
            cmd_str = "{}easycython {}/{}".format(scripts_path, "new_src", file_name)
            need_to_build_file_list.append(file_name)
            subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            progressBar.update()

    build_file_list = os.listdir()
    build_success_file_list = []
    for build_file in build_file_list:
        if build_file.split(".")[-1] == lib_suffix:
            shutil.copy(build_file,
                        os.path.join(ep_build_path, build_file.split(".")[0] + "." + lib_suffix))
            os.remove(build_file)
            build_success_file_list.append(build_file.split(".")[0] + ".py")

    for build_file in build_success_file_list:
        if build_file in need_to_build_file_list:
            need_to_build_file_list.remove(build_file)

    for need_to_build_file in need_to_build_file_list:
        try:
            print("\n{}文件编译失败,请使用easycython {}/{}重新编译".format(need_to_build_file, "src", need_to_build_file))
        except:
            print("\n{} file compile failed,please use easycython {}/{} recompile".format(need_to_build_file, "src", need_to_build_file))
        shutil.copy("{}/{}".format("new_src", need_to_build_file),
                    os.path.join(ep_build_path, need_to_build_file))

    if os.path.exists("src_copy"):
        shutil.rmtree("src_copy")

    if os.path.exists("new_src") is True:
        shutil.rmtree("new_src")

    if os.path.exists("{}.py".format(get_app_name(args))):
        os.remove("{}.py".format(get_app_name(args)))

    if os.path.exists("{}.spec".format(get_app_name(args))):
        os.remove("{}.spec".format(get_app_name(args)))
    if args.lib_path:
        if os.path.exists("build"):
            shutil.rmtree("build")


    save_path = CreateSavePath(os.path.join("releases", args.name + "V" + args.app_version))
    if os.path.exists("{}/{}".format(getOperationSystem(), save_path)) is True:
        shutil.rmtree("{}/{}".format(getOperationSystem(), save_path))
    save_bin_path = CreateSavePath(os.path.join(save_path, getOperationSystem()))
    # copy_dir("config", save_bin_path)
    if args.lib_path:
        copy_dir(args.lib_path, save_bin_path)


def recursion_dir(file_list, path):
    if os.path.isfile(path):
        file_list.append(path)
    else:
        for file_name in os.listdir(path):
            recursion_dir(file_list, os.path.join(path, file_name))


def get_uuid():
    return "{" + "{" + str(uuid.uuid1()) + "}"



def packSetup(args, exec_path, uuid,output_name=None):
    file_list = []
    recursion_dir(file_list, exec_path)
    if output_name is None:
        output_name =  get_app_name(args) + "_setup-V" + args.app_version[:-2] + "-" + args.app_version[-1]


    issname = "{}.iss".format(output_name)
    with open(issname, 'wb') as f:
        content = "; Script generated by the Inno Setup Script Wizard.\n" \
                  "; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!\n" \
                  "[Setup]\n" \
                  "; NOTE: The value of AppId uniquely identifies this application.\n" \
                  "; Do not use the same AppId value in installers for other applications.\n" \
                  "; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)\n" \
                  "VersionInfoVersion = {}\n" \
                  "AppCopyright = Copyright (C) 2019-{} Samples, Inc.\n" \
                  "AppId={}\n" \
                  ";应用名称\n" \
                  "AppName={}\n" \
                  ";应用版本号\n" \
                  "AppVersion={}\n" \
                  ";AppVerName={}\n" \
                  ";应用发布方\n" \
                  "AppPublisher=南京三宝科技有限公司\n" \
                  ";安装目录名称\n" \
                  "DefaultDirName={}\{}\n" \
                  "DefaultGroupName={}\n" \
                  ";安装目录不可选择\n" \
                  "DisableDirPage=yes\n" \
                  ";安装包文件名\n" \
                  "OutputBaseFilename={}\n" \
                  ";压缩包\n" \
                  "Compression=lzma\n" \
                  "SolidCompression=yes\n" \
                  ";安装包图标文件\n" \
                  "SetupIconFile={}\n" \
                  ";设置控制面板中程序图标\n" \
                  "UninstallDisplayIcon={}\n" \
                  ";设置控制面板中程序的名称\n" \
                  "UninstallDisplayName = {}\n" \
                  ";许可文件\n" \
                  ";LicenseFile=\n" \
                  "[Files]\n" \
                  ";安装文件\n" \
            .format(args.app_version, GetYear(), uuid, get_app_name(args), args.app_version, args.name,
                    "C:\\", get_app_name(args), get_app_name(args),
                   output_name,
                    os.path.abspath("icons/app_logo.ico"), os.path.abspath("icons/app_logo.ico"), args.name)

        for file in file_list:
            if len(file.split(exec_path)[-1].split("\\")) > 2:
                path = ""
                for p_file in file.split(exec_path)[-1].split("\\")[:-1]:
                    if p_file:
                        path = path + "\\" + p_file
                cmd_str = 'Source: "{}"; DestDir: "{}\\{}"; Flags: ignoreversion\n'.format(file, '{app}', path)
            else:
                cmd_str = 'Source: "{}"; DestDir: "{}\\{}"; Flags: ignoreversion \n'.format(file, '{app}', "")

            content = content + cmd_str
        content_back = ';[Registry]\n' \
                       ';开机启动\n' \
                       ';Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "MES Monitoring Client"; ValueData: """{}\Client\MES-MonitoringClient.exe"""; Flags: uninsdeletevalue\n' \
                       '[Icons]\n' \
                       'Name: "{}\{}"; Filename: "{}\{}"\n' \
                       'Name: "{}\{}"; Filename: "{}\{}"; Tasks: desktopicon;\n' \
                       '[Tasks]\n' \
                       'Name: "desktopicon"; Description: "{}"; GroupDescription: "{}"; Flags: checkablealone\n' \
                       '[run]\n' \
                       ';两种方法都可以安装服务，上面的可以将服务安装好，但不能直接运行\n' \
                       ';以下的方式可以直接运行，其中有Components:Service;当选中了服务才会安装服务\n' \
                       ';Flags:postinstall点击完成后，才会进行服务的安装，因为在处理RabbitMQ的服务器参数时，不会直接替换参数的\n' \
                       ';安装完成后启动应用\n' \
                       'Filename: "{}\{}"; Description: "{}";Flags:postinstall nowait skipifsilent \n' \
                       '[UninstallRun]\n' \
                       ';卸载时，停止服务并删除服务\n' \
                       ';Filename:{}\sc.exe; Parameters: "stop MESUploadDataService" ; Flags: runhidden; Components:Service\n' \
                       ';Filename: {}\sc.exe; Parameters: "delete MESUploadDataService" ; Flags: runhidden; Components:Service\n' \
                       '[Messages]\n' \
                       ';安装时，windows任务栏提示标题\n' \
                       'SetupAppTitle={}\n' \
                       ';安装时，安装引导标题\n' \
                       'SetupWindowTitle={}\n' \
                       ';在界面左下角加文字\n' \
                       'BeveledLabel=南京三宝科技有限公司\n' \
                       ';卸载对话框说明\n' \
                       'ConfirmUninstall=您真的想要从电脑中卸载 %1 吗?%n%n按 [是] 则完全删除 %1 以及它的所有组件;%n按 [否]则让软件继续留在您的电脑上.\n' \
                       ';[Types]\n' \
                       ';Name: "normaltype"; Description: "Normal Setup"\n' \
                       ';Name: "custom";     Description: "Custom Installation"; Flags: iscustom\n' \
                       ';[Components]\n' \
                       ';Name: "Client";     Description: "应用界面";  Types: normaltype custom\n' \
                       '[Code]\n' \
                       '//设置界面文字颜色\n' \
                       'procedure InitializeWizard();\n' \
                       'begin\n' \
                       '//WizardForm.WELCOMELABEL1.Font.Color:= clGreen;//设置开始安装页面第一段文字的颜色为绿色\n' \
                       '//WizardForm.WELCOMELABEL2.Font.Color:= clOlive;//设置开始安装页面第二段文字的颜色为橄榄绿\n' \
                       '//WizardForm.PAGENAMELABEL.Font.Color:= clRed;//设置许可协议页面第一段文字的颜色为红色\n' \
                       '//WizardForm.PAGEDESCRIPTIONLABEL.Font.Color:= clBlue; //设置许可协议页面第二段文字的颜色为蓝色\n' \
                       'WizardForm.MainPanel.Color:= clWhite;//设置窗格的颜色为白色\n' \
                       'end;\n' \
                       '//卸载后打开网址\n' \
                       '//procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);\n' \
                       '//var\n' \
                       '//  ErrorCode: Integer;\n' \
                       '//begin\n' \
                       '//  case CurUninstallStep of\n' \
                       '//   usUninstall:\n' \
                       '//     begin\n' \
                       '// 正在卸载\n' \
                       '//    end;\n' \
                       '//  usPostUninstall:\n' \
                       '//    begin\n' \
            .format("{app}",
                    "{group}", args.name, "{app}", get_app_name(args) + ".exe",
                    "{commondesktop}", args.name, "{app}", get_app_name(args) + ".exe",
                    "{cm:CreateDesktopIcon}", "{cm:AdditionalIcons}",
                    "{app}", get_app_name(args) + ".exe", "{" + "cm:LaunchProgram,{}".format(args.name) + "}",
                    "{sys}", "{sys}",
                    args.name + "-安装", args.name + "-安装")
        content = content + content_back
        content_code = "[Code]\n" \
                       "//;通过名称终结进程\n" \
                       "// 自定义函数，判断软件是否运行，参数为需要判断的软件的exe名称\n" \
                       "procedure CheckSoftRun(strExeName: String);\n" \
                       "// 变量定义\n" \
                       "var ErrorCode: Integer;\n" \
                       "var strCmdKill: String;  // 终止软件命令\n" \
                       "begin\n" \
                       "strCmdKill := Format('/c taskkill /f /t /im %s', [strExeName]);\n" \
                       "// 终止程序\n" \
                       "ShellExec('open', ExpandConstant('{}'), strCmdKill, '', SW_HIDE, ewNoWait, ErrorCode);\n" \
                       "end;\n" \
                       "function InitializeSetup(): Boolean;\n" \
                       "begin\n" \
                       " CheckSoftRun('{}');\n" \
                       "if (DirExists('{}\\{}')) then\n" \
                       "begin\n" \
                       "if MsgBox('是否要卸载旧版程序？', mbConfirmation, MB_YESNO) = IDYES then\n" \
                       "begin\n" \
                       "//删除文件夹及其中所有文件\n" \
                       "DelTree('{}\\{}', True, True, True);\n" \
                       "Result := True;\n" \
                       "end\n" \
                       "else\n" \
                       "begin\n" \
                       "Result := False;\n" \
                       "end;\n" \
                       "end\n" \
                       "else\n" \
                       "begin\n" \
                       "Result := True;\n" \
                       "end;\n" \
                       "end;\n".format("{cmd}", get_app_name(args) + ".exe", "C:", get_app_name(args), "C:",
                                       get_app_name(args))
        content = content + content_code
        f.write(content.encode("gbk"))
    inno_setup_path = os.path.join(GetPreviousDir(os.getcwd()), "InnoSetup")
    if os.path.exists(inno_setup_path):
        print("Inno Setup Path exists,dir:{}".format(inno_setup_path))
        cmd_str = "{} {}".format(os.path.join(inno_setup_path, "ISCC.exe"), os.path.join(os.getcwd(), issname))
        print("cmd str:{}".format(cmd_str))
        subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(os.path.join(os.getcwd(), issname))


def packAppImage(args):
    save_path = CreateSavePath(os.path.join("tmp"))
    save_bin_path = CreateSavePath(os.path.join(save_path, "usr/bin/"))
    if str_to_bool(args.full) is False:
        os.system("cp -r dist/{}/* {}".format(get_app_name(args), save_bin_path))
        ## 需要在AppRun中添加环境变量
    else:
        # 打包成一个包环境变量就没了
        save_lib_path = CreateSavePath(os.path.join(save_path, "usr/lib/"))
        if args.extra_path_list:
            for i in range(len(args.extra_path_list)):
                lib_path = args.extra_path_list[i]
                if type(lib_path) == tuple:
                    lib_path = lib_path[0]
                if os.path.isdir(lib_path):
                    for lib_name in os.listdir(lib_path):
                        if "lib" in lib_name:
                            shutil.copy(os.path.join(lib_path, lib_name), os.path.join(save_lib_path, lib_name))
        os.system("chmod a+x  dist/{}".format(get_app_name(args)))
        os.system("cp -r dist/{} {}".format(get_app_name(args), save_bin_path))


    with open(AppRunPath, "r") as f:
        conetent_list = f.read().split("\n")
        for content in conetent_list:
            with open(os.path.join(save_path, "AppRun"), "a", encoding="utf-8") as f:
                f.write(content + "\n")
    os.system("chmod a+x  {}".format(os.path.join(save_path, "AppRun")))
    if os.path.exists("icons/app_logo.png"):
        shutil.copy("icons/app_logo.png", save_path)
    else:
        shutil.copy(LogoPath, save_path)
    with open(os.path.join(save_path, get_app_name(args) + ".desktop"), "w", encoding="utf-8") as f:
        f.write("[Desktop Entry]\n"
                "Version={}\n"
                "Name={}\n"
                "Type=Application\n"
                "Categories=Qt;\n"
                "Terminal=false\n"
                "Icon=app_logo\n"
                "Exec={} %u\n"
                "MimeType=x-scheme-handler/qv2ray;\n"
                "X-AppImage-Version=912fe1b\n\n\n"
                "Name[zh_CN]={}".format("1.1", get_app_name(args), get_app_name(args), get_app_name(args)))
    os.system("chmod a+x  {}".format(os.path.join(save_path, get_app_name(args) + ".desktop")))
    print("{}/appimagetool-x86_64.AppImage {} {}.AppImage".format(os.path.expanduser("~"), "tmp", get_app_name(args)))
    os.system(
        "{}/appimagetool-x86_64.AppImage {} {}.AppImage".format(os.path.expanduser("~"), "tmp", get_app_name(args)))
    os.system("chmod a+x  {}.AppImage".format(get_app_name(args)))
    return "{}.AppImage".format(get_app_name(args))


def copy_dir(source_dir, save_path):
    try:
        shutil.rmtree("{}/{}".format(save_path, source_dir))
    except:
        pass
    try:
        shutil.copytree(source_dir, "{}/{}".format(save_path, source_dir))
    except:
        pass


def packAPP(args):
    writePy(args)
    write_version_info(args)
    writeSpec(args)
    scripts_path = ""
    try:
        if args.scripts_path:
            scripts_path = args.scripts_path + "/"
    except:
        pass
    python_version = (platform.python_version())
    if int(python_version.split(".")[1]) > 6:
        cmd_str = "{}pyinstaller  {}.spec ".format(scripts_path, get_app_name(args))
    else:
        cmd_str = "{}pyinstaller  {}.spec  --additional-hooks-dir hooks".format(scripts_path, get_app_name(args))

    os.system(cmd_str)
    save_path = CreateSavePath(os.path.join("releases", args.name + "V" + args.app_version))
    if os.path.exists("{}/{}".format(getOperationSystem(), save_path)) is True:
        shutil.rmtree("{}/{}".format(getOperationSystem(), save_path))
    save_bin_path = CreateSavePath(os.path.join(save_path, getOperationSystem()))
    # copy_dir("config", save_bin_path)
    if args.lib_path:
        copy_dir(args.lib_path, save_bin_path)
    if "Windows" == getOperationSystem():
        if str_to_bool(args.full) is False:
            cmd_str = "xcopy dist\\{} {} /s/y".format(get_app_name(args), save_bin_path)
            subprocess.run(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            shutil.copy("dist\\{}.exe".format(get_app_name(args)), "{}/".format(save_bin_path))
    else:
        if "Linux" == getOperationSystem():
            if str_to_bool(args.appimage):
                app_name = packAppImage(args)
                shutil.copy(app_name, "{}/".format(save_bin_path))
            else:
                if str_to_bool(args.full) is True:
                    shutil.copy("dist/{}".format(get_app_name(args)), "{}/".format(save_bin_path))
                else:
                    os.system("cp -r dist/{}/* {}/".format(get_app_name(args),(save_bin_path)))


        else:
            os.system("cp -r dist/{}.app {}".format(get_app_name(args), save_bin_path))
    if os.path.exists("{}.py".format(get_app_name(args))):
        os.remove("{}.py".format(get_app_name(args)))
    if os.path.exists("{}.spec".format(get_app_name(args))):
        os.remove("{}.spec".format(get_app_name(args)))

    if os.path.exists("new_src") is True:
        shutil.rmtree("new_src")

    if os.path.exists("build"):
        shutil.rmtree("build")

    if os.path.exists(args.lib_path):
        shutil.rmtree(args.lib_path)

    if os.path.exists("dist"):
        shutil.rmtree("dist")

    if os.path.exists("{}.AppImage".format(get_app_name(args))):
        os.remove("{}.AppImage".format(get_app_name(args)))

    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    if os.path.exists("file_verison_info.txt"):
        os.remove("file_verison_info.txt")

def get_app_version():
    try:
        with open("CONTRIBUTING.md","rb") as f:
            content = str(f.read(),encoding="utf-8").split("#### ")[1].split(" - ")[0]
            version = ""
            if "v" in content and "V" in content:
                version = content.split("V")[-1]
            elif "v" in content:
                version = content.split("v")[-1]
            elif "V" in content:
                version = content.split("V")[-1]
            if version:
                return version
            else:
                raise "please check CONTRIBUTING contain version"
    except:
        raise "please check CONTRIBUTING contain version"

def write_version(package_name):
    with open("{}/version.py".format(package_name),"wb") as f:
        f.write("full_version  = '{}'\n".format(get_app_version()).encode("utf-8"))

def zip_lib_package(args):
    CreateSavePath("Output")
    install_path = os.path.join(os.getcwd(),
                                "releases/{}/{}".format(args.name + "V" + args.app_version, getOperationSystem()))

    is_zip_lib = True
    try:
        is_zip_lib = str_to_bool(args.zip_lib)
    except:
        pass
    if is_zip_lib:
        zip_file(os.path.join(install_path, args.lib_path), os.path.join("Output/{}.zip".format(args.lib_path)))
    if os.path.exists(os.path.join(install_path,args.app_name)):
        shutil.copy(os.path.join(install_path,args.app_name),os.path.join("Output/{}".format(args.app_name)))

def zip_package(args):
    install_path = "releases/{}/{}/".format(args.name + "V" + args.app_version, getOperationSystem())
    CreateSavePath(os.path.join(install_path,"config"))
    shutil.copy(os.path.join("config","config.ini"),os.path.join(install_path,"config"))
    output_path = CreateSavePath("Output")
    if getOperationSystem() == "Windows":
        zip_file(install_path,"Output/{}-win32.zip".format(args.app_name + "V" + args.app_version))
    elif getOperationSystem() == "Linux":
        zip_file(install_path,"Output/{}-linux.zip".format(args.app_name + "V" + args.app_version))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    if getOperationSystem() == "Windows":
        parser.add_argument('--extra_sys_str', type=str,
                            default="")  ## 添加环境变量
        parser.add_argument('--extra_path_list', type=list,
                            default="")  ## 添加到exec打包路径
    else:
        parser.add_argument('--extra_sys_str', type=str,
                            default="")  ## 添加环境变量
        parser.add_argument('--extra_path_list', type=list,
                            default="")  ## 添加到exec打包路径

    parser.add_argument('--full', type=str,
                        default="False")  ## 打包成一个完成的包
    parser.add_argument("--use_jade_log", type=str, default="True")
    parser.add_argument('--console', type=str,
                        default="False")  ## 是否显示命令行窗口,只针对与Windows有效
    parser.add_argument('--app_version', type=str,
                        default="2.4.8.1")  ##需要打包的文件名称
    parser.add_argument('--app_name', type=str,
                        default="conta_service")  ##需要打包的文件名称
    parser.add_argument('--name', type=str,
                        default="箱号服务")  ##需要打包的文件名称
    parser.add_argument('--appimage', type=str,
                        default="False")  ## 是否打包成AppImage
    parser.add_argument('--is_qt', type=str, default="False")  ## 是否为Qt
    parser.add_argument("--specify_files", type=str, default="")
    parser.add_argument('--lib_path', type=str, default="conta_service_lib64")  ## 是否lib包分开打包

    args = parser.parse_args()
    # writePy(args)
    build(args)
    packAPP(args)
