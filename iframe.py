'''
To Handle iFrames in Selenium Webdriver we use switch_to

'''


#Using a WebElement 
#Switching using a WebElement is the most flexible option. You can find the frame using your 
#preferred selector and switch to it.
 # Store iframe web element
iframe = driver.find_element(By.CSS_SELECTOR, "#modal > iframe")

    # switch to selected iframe
driver.switch_to.frame(iframe)

    # Now click on button
driver.find_element(By.TAG_NAME, 'button').click()


#Using a name or ID
#If your frame or iframe has an id or name attribute, this can be used instead. If the name or 
#ID is not unique on the page, then the first one found will be switched to.
    # Switch frame by id
driver.switch_to.frame('buttonframe')

    # Now, Click on the button
driver.find_element(By.TAG_NAME, 'button').click()




#Using an index
#It is also possible to use the index of the frame, such as can be queried using window.frames in JavaScript.
    # switching to second iframe based on index
iframe = driver.find_elements(By.TAG_NAME,'iframe')[1]

    # switch to selected iframe
driver.switch_to.frame(iframe)
  


#Leaving a frame
#To leave an iframe or frameset, switch back to the default content like so:
 # switch back to default content
driver.switch_to.default_content()