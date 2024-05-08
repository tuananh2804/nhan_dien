try:
                #     image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()
                # except:
                #     continue
                    
                #     #waits to see if `esc` is pressed
                
                # if i == 4:
                #     res_tmp, score = predict(image_data)
                #     res = res_tmp
                #     i = 0
                #     if mem == res:
                #         consecutive += 1
                #     else:
                #         consecutive = 0
                #     if consecutive == 2 and res not in ['nothing']:
                #         if res == 'space':
                #             sequence += ' '
                #         elif res == 'del':
                #             sequence = sequence[:-1]
                #         else:
                #             sequence += res
                #         consecutive = 0
                # i += 1
                # cv2.putText(img, '%s' % (res.upper()), (100,400), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
                # cv2.putText(img, '(score = %.5f)' % (float(score)), (100,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
                # mem = res
                # cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
                # cv2.imshow("img", img)
                # img_sequence = np.zeros((200,1200,3), np.uint8)
                # cv2.putText(img_sequence, '%s' % (sequence.upper()), (30,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                # cv2.imshow('sequence', img_sequence)