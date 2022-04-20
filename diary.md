# Project Diary

> ### Week 1 (31st Jan - 6th Feb):
>
> Spent the week trying to iron out questions regarding the direction of the project, and trying to define some sort of goal/question to be answered, clarified
> nature of the report and continued wider research into image compression/quality assessment.

> ### Week 2 (7th Feb - 13th Feb):
> 
> Monday - Wednesday: continued to focus in on a topic for the report/research whilst continuing preliminary research to try and better understand image compression
> 
> Wednesday - Thursday: Write up for the project outline.
>
> Thursday: Started research into Image Quality Assessment Algorithms (IQAA) specifically.
> 
> Friday: Project outline submitted and continued reading into IQAA
> 
> Saturday - Sunday: Reading into IQAA

> ### Week 3 (14th Feb - 20th Feb):
> 
> Monday - Saturday: Reading into IQAA, also looked into creating bitmaps from images (thinking ahead to when trying to write scripts for data analysis)
>
> Saturday: Created a short test script to convert PNG to BMP, development for when statistical analysis is required
> 
> Sunday: More reading - also added functionality to script to create text file with pixel values, helps to calculate MSE for IQAA (Still need to find how to do
> this for non-bmp image files)
> 
>         Developed understanding for Mean Square Error (MSE) and therefore as by-product Root Mean Square Error (RMSE) and Peak Signal to Noise Ratio (PSNR) - 
>         along with development of basic test script now have primitive method of conducting pixel to pixel analysis on at least PNG and BMP images.

> ### Week 4 (21st Feb - 27th Feb):
> 
> Monday - Sunday: Reading

> ### Week 5 (28th Feb - 6th March):
>
> Monday - Thursday: Reading
>
> Friday: Minor updates to report template (pulled changes from module GitLab)
>
> Saturday: Major updates to development script to incorporate MSE calculation and tested against PNG/BMP/JPG varaiants of the same image
>
>         Script needs some refactoring/tidying-up, JPG image variant was acquired using online converter at this location: https://www.freeconvert.com/
>         assumption made that standard JPG conversion algorithm used, minimum testing done to validate that there is no difference between PNG and BMP (and
>         results) in MSE of 0.0, and there is difference between PNG and JPG and so MSE > 0.

> ### Week 6 (7th Mar - 13th Mar):
>
> Monday - Source came through from the library, have begun reading this, also continued general reading process and found good potential source on subjective assessment
> methods, also cleaned up script
>
> Tuesday - Sunday: Reading

> ### Week 7 (14th Mar - 20th Mar):
>
> Monday - Tuesday: Reading
>
> Wednesday: Converted first sampole image to JPG using script. Checked details using image inspect tool (macOS Preview tool), moreover conducted some basic
> analysis using the script constructed in the first few weeks of the project to find MSE. Can develop further to get PSNR and other basic IQAAs.
>
> Thursday: Reading
>
> Friday: Began writing report
>
> Saturday - Sunday: Reading, continued writing report, and prep for mid project demo

> ### Week 8 (21st Mar - 27th Mar):
> 
> Monday: Prep for mid project demo
> 
> Tuesday: Mid Project demo
>
> Wednesday - Sunday: Actioning some of the feedback from the mid project demo to improve script and understanding of direction of project

> ### Week 9 (28th Mar - 3rd Apr):
>
> Monday - Sunday: Progress was overall quite slow, issues with script but mainly access to materials needed to proceed with project. Started developing
>                  contingency plans for possible project change, planned parts of report that am able to write at this stage but this is also quite
>                  limited

================================ PROJECT CHANGE ================================

> ### Week 10 & 11 (4th Apr - 17th Apr):
>
> Spent these two weeks collecting data for BPE (Bit Plane Encoder) at 8x and 80x compression and J2K (also at 8 and 80 times) compression algos and
> generating tables of results for both algorithms and compression ratios - collected information such as:
> 
>   Original filesize/Time to encode and decode/compressed size/MSE, PSNR, and SSIM when compared o the original image
>
> Was unable to achieve compression and/or comparative analysis with RGBA images but still have plenty of data to work with but this must be mentioned in
> report. Achieved this process semi autonomously through bash commands and used the in-progress Python script to calculate Image Quality.

> ### Week 12 (18th Apr - 24th Apr):
>
> Monday - Tuesday: Corrected some issues with incorrectly collected data so had to re-process images to find certain information that was originally
>                   incorrect.
>
> Wednesday: Planned and started working on collection of statistics that will help to inform answer to research question, moreover started writing report
