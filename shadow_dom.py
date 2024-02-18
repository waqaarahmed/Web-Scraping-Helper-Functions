'''
To Handle Shadow Dom elements with Selenium:
1-Finding the shadow root element.
2-Using the shadow root as a driver to interact with elements inside it.'''

#First way
# Execute JavaScript to get the shadow root
shadow_root_script = "return document.querySelector('#shadow-root-wrapper').shadowRoot"
shadow_root = driver.execute_script(shadow_root_script)

# Find an element within the shadow root using CSS Selector
element_in_shadow_dom = shadow_root.find_element(By.CSS_SELECTOR, '<locator>')        




#Second Way
# Find the element wrapping the shadow DOM
shadow_root_wrapper = driver.find_element(By.CSS_SELECTOR, '#shadow-root-wrapper')

# Access the shadow root of the element
shadow_root = shadow_root_wrapper.shadow_root

# Find an element within the shadow root using CSS Selector
element_in_shadow_dom = shadow_root.find_element(By.CSS_SELECTOR, '<locator>')        