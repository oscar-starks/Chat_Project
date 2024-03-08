from common.responses import CustomSuccessResponse

def customPaginator(request, serializer, data, page_number):
    data_len = data.count()

    if page_number <= 1:
        data = data[:10]
        pageEnd = (page_number*10)
        page_subtraction = data_len-pageEnd

    else:
        pageOffset = (page_number-1)*10
        pageEnd = (page_number*10)
        data = data[pageOffset:pageEnd]
        page_subtraction = data_len-pageEnd

    serializer = serializer(data, many=True, context = {"request": request})
    return CustomSuccessResponse(data={"message": "data fetched!", "data": serializer.data, "has_next":page_subtraction > 0})
