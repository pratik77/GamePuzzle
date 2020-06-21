class Response:
    def response(self, responseCode,hasError,data,message):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['hasError'] = hasError
        response['data'] = data
        return response

    def errorResponse(self, err):
        print(err)
        message = str(err)
        return self.response("503", "true",{}, message)