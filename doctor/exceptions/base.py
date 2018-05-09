# -*- coding：utf-8 -*-


class DoctorException(Exception):
    code = -1
    msg = '错误'

    def to_result(self):
        return {'code': self.code, 'msg': self.msg}
