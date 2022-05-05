import logging

logger = logging.getLogger('file_upload')

#####################################################################################
# 関数名：P01.print_log（Ｐ０１Ａ）
# 関数概要：ログを出力する。
#####################################################################################
def print_log(lmessage, ltype):
    print(lmessage)
    if ltype == 'INFO':
        logger.info(lmessage)
    elif ltype == 'WARN':
        logger.warn(lmessage)
    elif ltype == 'ERROR':
        logger.error(lmessage)
    else:
        logger.error(lmessage)
