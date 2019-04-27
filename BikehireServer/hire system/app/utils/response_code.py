
class RET:
    OK                  = "0"
    DBERR               = "4001"
    NODATA              = "4002"
    DATAEXIST           = "4003"
    DATAERR             = "4004"
    SESSIONERR          = "4101"
    LOGINERR            = "4102"
    PARAMERR            = "4103"
    USERERR             = "4104"
    ROLEERR             = "4105"
    PWDERR              = "4106"
    REQERR              = "4201"
    IPERR               = "4202"
    IOERR               = "4302"
    SERVERERR           = "4500"
    UNKOWNERR           = "4501"

error_map = {
    RET.OK                    : u"success",
    RET.DBERR                 : u"database error",
    RET.NODATA                : u"no date exited",
    RET.DATAEXIST             : u"date exited",
    RET.DATAERR               : u"data error",
    RET.SESSIONERR            : u"user no login",
    RET.LOGINERR              : u"login failed",
    RET.PARAMERR              : u"parament error",
    RET.USERERR               : u"user error",
    RET.ROLEERR               : u"role error",
    RET.PWDERR                : u"password error",
    RET.REQERR                : u"Illegal request",
    RET.IPERR                 : u"IP error",
    RET.IOERR                 : u"IO error",
    RET.SERVERERR             : u"server error",
    RET.UNKOWNERR             : u"unknown error",
}