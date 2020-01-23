import streamlit as st
import pages.userinterface
import pages.biography
import pages.instagram
import pages.about
import pages.technology
import pages.admininterface


PAGES = {
    "User Interface": pages.userinterface,
    "Biography Generation": pages.biography,
    "Instagram Classification": pages.instagram,
    "Admin Interface": pages.admininterface,
    "Technologies": pages.technology,
    "About": pages.about,
}


def main():
    st.sidebar.info("**Les Quiromanciers**")
    page = st.sidebar.radio("Menu", options=list(PAGES.keys()))
    st.title(page)
    PAGES[page].content()


if __name__ == "__main__":
    main()
