# ref [https://medium.com/hackernoon/create-lean-node-js-image-with-docker-multi-stage-build-252e927cbf3e]
#
# ---- Base Node ----
FROM node:lts AS base
# install node
# set working directory
WORKDIR /root/chat
# Set tini as entrypoint
ENTRYPOINT ["/sbin/tini", "--"]
# copy project file
COPY package.json .
 
#
# ---- Dependencies ----
FROM base AS dependencies
# install node packages
RUN npm set progress=false && npm config set depth 0
RUN npm install --only=production  --force -i
# copy production node_modules aside
RUN cp -R node_modules prod_node_modules
# install ALL node_modules, including 'devDependencies'
RUN npm install -i --force
 
# #
# # ---- Test ----
# # run linters, setup and tests
# FROM dependencies AS test
# COPY . .
# # RUN  npm run && npm run setup && npm run test
# RUN  npm run && npm run setup 
 
#
# ---- Release ----
FROM base AS release
# copy production node_modules
COPY --from=dependencies /root/chat/prod_node_modules ./node_modules
# copy app sources
RUN apt-get update
RUN apt-get install tini -y
RUN mv /usr/bin/tini /sbin/tini
COPY . .
RUN npx next build
# expose port and define CMD
EXPOSE 3000
CMD npm start
